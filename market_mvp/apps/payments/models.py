from django.conf import settings
from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    GATEWAY_CLICK = 'click'
    GATEWAY_PAYME = 'payme'
    GATEWAY_UZUM = 'uzum'

    GATEWAY_CHOICES = [
        (GATEWAY_CLICK, 'Click'),
        (GATEWAY_PAYME, 'Payme'),
        (GATEWAY_UZUM, 'Uzum'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SUCCESS, 'Success'),
        (STATUS_FAILED, 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    order_id = models.PositiveIntegerField(null=True, blank=True)
    gateway = models.CharField(max_length=32, choices=GATEWAY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default='UZS')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reference = models.CharField(max_length=255, blank=True)
    payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.gateway} txn {self.id} - {self.amount} {self.currency} ({self.status})"
