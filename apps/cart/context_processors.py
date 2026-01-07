"""
Cart context processor to make cart available in all templates.
"""
from .models import Cart


def cart(request):
    """
    Add cart to template context.
    """
    if request.user.is_authenticated:
        try:
            user_cart = Cart.objects.get(user=request.user)
            cart_count = user_cart.items_count
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        cart_count = 0

    return {
        'cart_count': cart_count,
    }