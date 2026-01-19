"""
Order service layer.
Business logic for order management.
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from .models import Order, OrderItem, OrderStatusHistory
from apps.cart.models import Cart


class OrderService:
    """
    Service for managing order operations.
    Implements business logic and validation.
    """

    @transaction.atomic
    def create_order_from_cart(self, user, cart: Cart, checkout_data: dict, currency: str = 'UZS') -> Order:
        """
        Create order from shopping cart.

        Args:
            user: User placing the order
            cart: Shopping cart
            checkout_data: Checkout form data
            currency: Order currency

        Returns:
            Created Order instance
        """
        if checkout_data.get('use_saved_address') and checkout_data.get('saved_address'):
            address = checkout_data['saved_address']
            delivery_address = address.full_address
            delivery_city = address.city
            delivery_region = address.region
            latitude = address.latitude
            longitude = address.longitude
        else:
            delivery_address = checkout_data['delivery_address']
            delivery_city = checkout_data['delivery_city']
            delivery_region = checkout_data.get('delivery_region', '')
            latitude = checkout_data.get('latitude')
            longitude = checkout_data.get('longitude')

        subtotal = cart.get_total(currency)
        delivery_fee = self._calculate_delivery_fee(delivery_city)
        tax_amount = Decimal('0')
        discount_amount = Decimal('0')
        total_amount = subtotal + delivery_fee + tax_amount - discount_amount

        order = Order.objects.create(
            user=user,
            customer_name=checkout_data['customer_name'],
            customer_email=checkout_data['customer_email'],
            customer_phone=checkout_data['customer_phone'],
            delivery_address=delivery_address,
            delivery_city=delivery_city,
            delivery_region=delivery_region,
            latitude=latitude,
            longitude=longitude,
            currency=currency,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            tax_amount=tax_amount,
            discount_amount=discount_amount,
            total_amount=total_amount,
            payment_method=checkout_data['payment_method'],
            customer_notes=checkout_data.get('customer_notes', ''),
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.sku,
                unit_price=cart_item.price_snapshot,
                quantity=cart_item.quantity,
                subtotal=cart_item.get_subtotal()
            )

            cart_item.product.stock -= cart_item.quantity
            cart_item.product.sales_count += cart_item.quantity
            cart_item.product.save(update_fields=['stock', 'sales_count'])

        OrderStatusHistory.objects.create(
            order=order,
            to_status=Order.STATUS_PENDING,
            changed_by=user
        )

        return order

    def _calculate_delivery_fee(self, city: str) -> Decimal:
        """
        Calculate delivery fee based on city.
        Implement your delivery pricing logic here.
        """
        if city.lower() in ['tashkent', 'toshkent']:
            return Decimal('20000')
        else:
            return Decimal('35000')

    @transaction.atomic
    def update_order_status(self, order: Order, new_status: str, user, notes: str = ''):
        """
        Update order status with history tracking.
        """
        old_status = order.status
        order.status = new_status

        if new_status == Order.STATUS_DELIVERED:
            order.delivered_at = timezone.now()

        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            from_status=old_status,
            to_status=new_status,
            changed_by=user,
            notes=notes
        )

        from core.services.email import EmailService
        EmailService().send_order_status_update(order)

    @transaction.atomic
    def mark_order_as_paid(self, order: Order):
        """
        Mark order as paid and send invoice email.
        
        Args:
            order: Order instance to mark as paid
        """
        if order.is_paid:
            return

        order.is_paid = True
        order.paid_at = timezone.now()
        order.save(update_fields=['is_paid', 'paid_at'])

        from core.services.email import EmailService
        email_service = EmailService()
        email_service.send_order_invoice(order, attach_pdf=True)

        if order.status == Order.STATUS_PENDING:
            email_service.send_order_confirmation(order)
