from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.orders.models import Order
from django.core import mail


class DashboardTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.staff = User.objects.create_user(username='admin', password='pass', is_staff=True)
        self.order = Order.objects.create(first_name='A', email='a@example.com', address_line1='addr', total=10)

    def test_stats_endpoint_requires_staff(self):
        resp = self.client.get(reverse('dashboard:stats'))
        self.assertIn(resp.status_code, (302, 403))
        self.client.force_login(self.staff)
        resp = self.client.get(reverse('dashboard:stats'))
        self.assertEqual(resp.status_code, 200)

    def test_order_action_requires_post(self):
        self.client.force_login(self.staff)
        url = reverse('dashboard:order_action', args=[self.order.id, 'ship'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 400)

    def test_order_action_creates_orderaction_and_emails(self):
        self.client.force_login(self.staff)
        url = reverse('dashboard:order_action', args=[self.order.id, 'ship'])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        from apps.orders.models import OrderAction
        actions = OrderAction.objects.filter(order=self.order, action=OrderAction.ACTION_SHIP)
        self.assertTrue(actions.exists())
        self.assertGreaterEqual(len(mail.outbox), 1)
