"""
Cart context processor to make cart available in all templates.
"""
from .models import Cart


def cart(request):
    """
    Add cart to template context.
    """
    user = getattr(request, 'user', None)
    if user and hasattr(user, 'is_authenticated') and user.is_authenticated:
        try:
            user_cart = Cart.objects.get(user=user)
            cart_count = user_cart.items_count
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        cart_count = 0

    return {
        'cart_count': cart_count,
    }
