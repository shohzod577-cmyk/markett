"""
Shopping cart service layer.
Business logic for cart operations.
"""
from decimal import Decimal
from django.db import transaction

from .models import Cart, CartItem
from apps.products.models import Product, ProductVariant


class CartService:
    """
    Service for managing shopping cart operations.
    """

    def __init__(self, user):
        self.user = user

    def get_cart(self):
        """Get or create cart for user."""
        cart, created = Cart.objects.get_or_create(user=self.user)
        return cart

    @transaction.atomic
    def add_item(self, product: Product, quantity: int = 1, variant: ProductVariant = None):
        """
        Add item to cart or update quantity if exists.
        """
        cart = self.get_cart()

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

    @transaction.atomic
    def update_item(self, cart_item_id: int, quantity: int):
        """
        Update cart item quantity.
        """
        cart = self.get_cart()
        cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)

        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

    @transaction.atomic
    def remove_item(self, cart_item_id: int):
        """
        Remove item from cart.
        """
        cart = self.get_cart()
        CartItem.objects.filter(id=cart_item_id, cart=cart).delete()

    @transaction.atomic
    def clear_cart(self):
        """
        Remove all items from cart.
        """
        cart = self.get_cart()
        cart.clear()

    def get_cart_total(self, currency='UZS') -> Decimal:
        """
        Calculate cart total in specified currency.
        """
        cart = self.get_cart()
        return cart.get_total(currency)