"""
Order models for Market e-commerce platform.
Comprehensive order management with state machine pattern.
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal

from apps.products.models import Product, ProductVariant


class Order(models.Model):
    """
    Order model representing a customer purchase.
    Central model for order lifecycle management.
    """

    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_PACKED = 'packed'
    STATUS_ON_THE_WAY = 'on_the_way'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_ACCEPTED, _('Accepted')),
        (STATUS_PACKED, _('Packed')),
        (STATUS_ON_THE_WAY, _('On the way')),
        (STATUS_DELIVERED, _('Delivered')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]

    order_number = models.CharField(
        _('order number'),
        max_length=50,
        unique=True,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('user')
    )

    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    customer_name = models.CharField(_('customer name'), max_length=200)
    customer_email = models.EmailField(_('customer email'))
    customer_phone = models.CharField(_('customer phone'), max_length=20)

    delivery_address = models.TextField(_('delivery address'))
    delivery_city = models.CharField(_('city'), max_length=100)
    delivery_region = models.CharField(_('region'), max_length=100, blank=True)

    latitude = models.DecimalField(
        _('latitude'),
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        _('longitude'),
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    currency = models.CharField(
        _('currency'),
        max_length=3,
        default='UZS'
    )

    subtotal = models.DecimalField(
        _('subtotal'),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    delivery_fee = models.DecimalField(
        _('delivery fee'),
        max_digits=10,
        decimal_places=2,
        default=0
    )

    tax_amount = models.DecimalField(
        _('tax amount'),
        max_digits=10,
        decimal_places=2,
        default=0
    )

    discount_amount = models.DecimalField(
        _('discount amount'),
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        _('total amount'),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    payment_method = models.CharField(
        _('payment method'),
        max_length=50,
        choices=[
            ('cash', _('Cash on Delivery')),
            ('card', _('Plastic Card')),
            ('click', _('Click')),
            ('payme', _('Payme')),
            ('uzum', _('Uzum Bank')),
        ]
    )

    is_paid = models.BooleanField(_('paid'), default=False)
    paid_at = models.DateTimeField(_('paid at'), blank=True, null=True)

    customer_notes = models.TextField(_('customer notes'), blank=True)
    admin_notes = models.TextField(_('admin notes'), blank=True)

    cancelled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='cancelled_orders',
        blank=True,
        null=True,
        verbose_name=_('cancelled by')
    )
    cancellation_reason = models.TextField(_('cancellation reason'), blank=True)
    cancelled_at = models.DateTimeField(_('cancelled at'), blank=True, null=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    delivered_at = models.DateTimeField(_('delivered at'), blank=True, null=True)

    class Meta:
        db_table = 'orders'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Order #{self.order_number}"

    def save(self, *args, **kwargs):
        """Generate order number if not exists."""
        if not self.order_number:
            import uuid
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid.uuid4().hex)[:6].upper()
            self.order_number = f"ORD-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)

    @property
    def can_be_cancelled(self):
        """Check if order can be cancelled by customer."""
        return self.status in [self.STATUS_PENDING, self.STATUS_ACCEPTED, self.STATUS_PACKED]

    @property
    def is_completed(self):
        """Check if order is completed."""
        return self.status == self.STATUS_DELIVERED

    @property
    def items_count(self):
        """Return total number of items in order."""
        return sum(item.quantity for item in self.items.all())

    def calculate_total(self):
        """Calculate and update order total."""
        self.subtotal = sum(item.get_subtotal() for item in self.items.all())
        self.total_amount = self.subtotal + self.delivery_fee + self.tax_amount - self.discount_amount
        self.save(update_fields=['subtotal', 'total_amount'])

    def mark_as_paid(self):
        """Mark order as paid."""
        from django.utils import timezone
        self.is_paid = True
        self.paid_at = timezone.now()
        self.save(update_fields=['is_paid', 'paid_at'])

    def cancel(self, user, reason):
        """Cancel the order."""
        from django.utils import timezone
        if not self.can_be_cancelled:
            raise ValueError("Order cannot be cancelled at this stage")

        self.status = self.STATUS_CANCELLED
        self.cancelled_by = user
        self.cancellation_reason = reason
        self.cancelled_at = timezone.now()
        self.save(update_fields=['status', 'cancelled_by', 'cancellation_reason', 'cancelled_at'])

        for item in self.items.all():
            item.product.stock += item.quantity
            item.product.save(update_fields=['stock'])


class OrderItem(models.Model):
    """
    Individual item within an order.
    Snapshot of product at time of purchase.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('order')
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=_('product')
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_('variant')
    )

    product_name = models.CharField(_('product name'), max_length=255)
    product_sku = models.CharField(_('SKU'), max_length=100)

    unit_price = models.DecimalField(
        _('unit price'),
        max_digits=15,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(
        _('quantity'),
        validators=[MinValueValidator(1)]
    )

    subtotal = models.DecimalField(
        _('subtotal'),
        max_digits=15,
        decimal_places=2
    )

    class Meta:
        db_table = 'order_items'
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    def get_subtotal(self):
        """Calculate subtotal for this item."""
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        """Snapshot product data and calculate subtotal."""
        if not self.product_name:
            self.product_name = self.product.name
            self.product_sku = self.product.sku

        if not self.subtotal:
            self.subtotal = self.get_subtotal()

        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    """
    Track order status changes for audit trail.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='status_history',
        verbose_name=_('order')
    )

    from_status = models.CharField(_('from status'), max_length=20, blank=True)
    to_status = models.CharField(_('to status'), max_length=20)

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('changed by')
    )

    notes = models.TextField(_('notes'), blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        db_table = 'order_status_history'
        verbose_name = _('Order Status History')
        verbose_name_plural = _('Order Status Histories')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order.order_number}:  {self.from_status} → {self.to_status}"