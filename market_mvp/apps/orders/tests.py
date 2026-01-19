from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model
from apps.products.models import Category, Product
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order


class OrdersTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='cust', password='pass')
        c = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(title='Phone', slug='phone', sku='P-001', price=50, currency='UZS', category=c)

        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_checkout_creates_order_and_clears_cart(self):
        self.client.force_login(self.user)
        url = reverse('orders:checkout')
        data = {
            'first_name': 'Alice',
            'email': 'alice@example.com',
            'address_line1': 'Some address',
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        order = Order.objects.filter(email='alice@example.com').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items_count, 2)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items.count(), 0)
from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.products.models import Category, Product
from apps.cart.models import Cart, CartItem
from .models import Order


class OrderModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='tester', email='t@example.com', password='pass')
        c = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(title='Phone', slug='phone', sku='P-001', price=100, currency='UZS', category=c)

    def test_create_order_from_cart(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        customer = {
            'first_name': 'Test', 'last_name': 'User', 'email': 't@example.com',
            'address_line1': 'Street 1'
        }
        order = Order.create_from_cart(cart, customer)
        self.assertEqual(order.total, 200)
        self.assertEqual(order.items_count, 2)
