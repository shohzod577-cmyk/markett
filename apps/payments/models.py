"""
Payment models for Market e-commerce platform.
Supports multiple payment gateways and transaction tracking.
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from decimal import Decimal

from apps.orders.models import Order


class Payment(models.Model):
    """
    Payment model tracking all payment transactions.
    Gateway-agnostic design for multiple payment providers.
    """

    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_REFUNDED = 'refunded'

    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_PROCESSING, _('Processing')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_FAILED, _('Failed')),
        (STATUS_CANCELLED, _('Cancelled')),
        (STATUS_REFUNDED, _('Refunded')),
    ]

    GATEWAY_CASH = 'cash'
    GATEWAY_CARD = 'card'
    GATEWAY_CLICK = 'click'
    GATEWAY_PAYME = 'payme'
    GATEWAY_UZUM = 'uzum'

    GATEWAY_CHOICES = [
        (GATEWAY_CASH, _('Cash on Delivery')),
        (GATEWAY_CARD, _('Plastic Card')),
        (GATEWAY_CLICK, _('Click')),
        (GATEWAY_PAYME, _('Payme')),
        (GATEWAY_UZUM, _('Uzum Bank')),
    ]

    payment_id = models.CharField(
        _('payment ID'),
        max_length=100,
        unique=True,
        editable=False
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name=_('order')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name=_('user')
    )

    gateway = models.CharField(
        _('payment gateway'),
        max_length=20,
        choices=GATEWAY_CHOICES
    )

    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    amount = models.DecimalField(
        _('amount'),
        max_digits=15,
        decimal_places=2
    )

    currency = models.CharField(_('currency'), max_length=3, default='UZS')

    gateway_transaction_id = models.CharField(
        _('gateway transaction ID'),
        max_length=200,
        blank=True,
        null=True
    )

    gateway_response = models.JSONField(
        _('gateway response'),
        blank=True,
        null=True,
        help_text='Raw response from payment gateway'
    )

    card_number_masked = models.CharField(
        _('masked card number'),
        max_length=20,
        blank=True,
        null=True
    )

    card_type = models.CharField(
        _('card type'),
        max_length=50,
        blank=True,
        null=True
    )

    ip_address = models.GenericIPAddressField(_('IP address'), blank=True, null=True)
    user_agent = models.TextField(_('user agent'), blank=True)

    error_code = models.CharField(_('error code'), max_length=50, blank=True)
    error_message = models.TextField(_('error message'), blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    completed_at = models.DateTimeField(_('completed at'), blank=True, null=True)

    class Meta:
        db_table = 'payments'
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_id']),
            models.Index(fields=['order']),
            models.Index(fields=['status']),
            models.Index(fields=['gateway_transaction_id']),
        ]

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"

    def save(self, *args, **kwargs):
        """Generate payment ID if not exists."""
        if not self.payment_id:
            import uuid
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid.uuid4().hex)[:8].upper()
            self.payment_id = f"PAY-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)

    def mark_as_completed(self, transaction_id=None):
        """Mark payment as completed."""
        self.status = self.STATUS_COMPLETED
        self.completed_at = timezone.now()
        if transaction_id:
            self.gateway_transaction_id = transaction_id
        self.save(update_fields=['status', 'completed_at', 'gateway_transaction_id'])

        self.order.mark_as_paid()

    def mark_as_failed(self, error_code='', error_message=''):
        """Mark payment as failed."""
        self.status = self.STATUS_FAILED
        self.error_code = error_code
        self.error_message = error_message
        self.save(update_fields=['status', 'error_code', 'error_message'])

    @property
    def is_successful(self):
        """Check if payment was successful."""
        return self.status == self.STATUS_COMPLETED


class Transaction(models.Model):
    """
    Detailed transaction log for payment operations.
    Provides audit trail for all payment-related events.
    """

    TYPE_AUTHORIZATION = 'authorization'
    TYPE_CAPTURE = 'capture'
    TYPE_REFUND = 'refund'
    TYPE_VOID = 'void'
    TYPE_WEBHOOK = 'webhook'

    TYPE_CHOICES = [
        (TYPE_AUTHORIZATION, _('Authorization')),
        (TYPE_CAPTURE, _('Capture')),
        (TYPE_REFUND, _('Refund')),
        (TYPE_VOID, _('Void')),
        (TYPE_WEBHOOK, _('Webhook')),
    ]

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name=_('payment')
    )

    transaction_type = models.CharField(
        _('transaction type'),
        max_length=20,
        choices=TYPE_CHOICES
    )

    amount = models.DecimalField(
        _('amount'),
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
    )

    status = models.CharField(_('status'), max_length=50)

    gateway_transaction_id = models.CharField(
        _('gateway transaction ID'),
        max_length=200,
        blank=True
    )

    request_data = models.JSONField(_('request data'), blank=True, null=True)
    response_data = models.JSONField(_('response data'), blank=True, null=True)

    ip_address = models.GenericIPAddressField(_('IP address'), blank=True, null=True)
    notes = models.TextField(_('notes'), blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        db_table = 'transactions'
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} - {self.payment.payment_id}"