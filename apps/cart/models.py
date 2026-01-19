"""
Shopping cart models for Market platform.
Supports persistent carts for authenticated users.
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from apps.products.models import Product, ProductVariant


class Cart(models.Model):
    """
    Shopping cart for authenticated users.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_('user')
    )

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        db_table = 'carts'
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f"Cart of {self.user.email}"

    @property
    def items_count(self):
        """Return total number of items in cart."""
        return sum(item.quantity for item in self.items.all())

    def get_total(self, currency='UZS'):
        """
        Calculate cart total in specified currency.
        Uses currency service for conversion.
        """
        from core.services.currency import CurrencyService

        total = sum(item.get_subtotal() for item in self.items.all())

        if currency != 'UZS':
            currency_service = CurrencyService()
            total = currency_service.convert(total, 'UZS', currency)

        return total

    def clear(self):
        """Remove all items from cart."""
        self.items.all().delete()


class CartItem(models.Model):
    """
    Individual item in shopping cart.
    """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('cart')
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product')
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('variant')
    )

    quantity = models.PositiveIntegerField(
        _('quantity'),
        default=1,
        validators=[MinValueValidator(1)]
    )

    price_snapshot = models.DecimalField(
        _('price snapshot'),
        max_digits=15,
        decimal_places=2
    )

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        db_table = 'cart_items'
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')
        unique_together = ['cart', 'product', 'variant']

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    def get_subtotal(self):
        """Calculate subtotal for this cart item."""
        return self.price_snapshot * self.quantity

    def save(self, *args, **kwargs):
        """Set price snapshot if not already set."""
        if not self.price_snapshot:
            self.price_snapshot = self.product.discounted_price
            if self.variant:
                self.price_snapshot += self.variant.price_adjustment
        super().save(*args, **kwargs)