import json
from django.test import TestCase

from apps.orders.models import Order
from apps.products.models import Category, Product
from apps.payments.models import Transaction
from django.core import mail


class PaymentsWebhookTests(TestCase):
    def setUp(self):
        c = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(title='Phone', slug='phone', sku='P-001', price=50, currency='UZS', category=c)
        self.order = Order.objects.create(first_name='A', email='a@example.com', address_line1='addr', total=100)

    def test_click_webhook_marks_order_paid(self):
        payload = {'order_id': str(self.order.id), 'status': 'success', 'amount': 100}
        resp = self.client.post('/payments/webhook/click/', json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.STATUS_PAID)
        txn = Transaction.objects.filter(reference=str(self.order.id)).first()
        self.assertIsNotNone(txn)
        self.assertEqual(txn.status, Transaction.STATUS_SUCCESS)
        self.assertGreaterEqual(len(mail.outbox), 1)
