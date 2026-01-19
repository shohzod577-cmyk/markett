from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.products.models import Product, ProductVariant


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_PROCESSING = 'processing'
    STATUS_SHIPPED = 'shipped'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELED, 'Canceled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    postal_code = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=80, default='Uzbekistan')

    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.email} ({self.status})"

    @property
    def items_count(self):
        return self.items.aggregate(count=models.Sum('quantity'))['count'] or 0

    @classmethod
    def create_from_cart(cls, cart, customer_data):
        order = cls.objects.create(
            user=cart.user if cart.user_id else None,
            first_name=customer_data.get('first_name', ''),
            last_name=customer_data.get('last_name', ''),
            email=customer_data.get('email', ''),
            phone=customer_data.get('phone', ''),
            address_line1=customer_data.get('address_line1', ''),
            address_line2=customer_data.get('address_line2', ''),
            city=customer_data.get('city', ''),
            postal_code=customer_data.get('postal_code', ''),
            country=customer_data.get('country', 'Uzbekistan'),
        )

        total = 0
        for ci in cart.items.select_related('product', 'variant').all():
            price = ci.variant.price if ci.variant else ci.product.price
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                variant=ci.variant,
                price=price,
                quantity=ci.quantity,
            )
            total += price * ci.quantity

        order.total = total
        order.save()
        return order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} @ {self.price}"


class OrderAction(models.Model):
    ACTION_SHIP = 'ship'
    ACTION_CANCEL = 'cancel'
    ACTION_CHOICES = [
        (ACTION_SHIP, 'Shipped'),
        (ACTION_CANCEL, 'Canceled'),
    ]

    order = models.ForeignKey(Order, related_name='actions', on_delete=models.CASCADE)
    action = models.CharField(max_length=32, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"OrderAction {self.action} on #{self.order_id} by {self.performed_by}"
