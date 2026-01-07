"""
Shopping cart views.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .services import CartService
from apps.products.models import Product, ProductVariant


@login_required
def cart_view(request):
    """
    Display shopping cart.
    """
    cart_service = CartService(request.user)
    cart = cart_service.get_cart()

    # Get currency from session
    currency = request.session.get('currency', 'UZS')
    total = cart.get_total(currency) if cart else 0

    context = {
        'cart': cart,
        'total': total,
        'currency': currency,
    }

    return render(request, 'cart/cart.html', context)


@login_required
@require_http_methods(["POST"])
def add_to_cart_view(request, product_id):
    """
    Add product to cart.
    """
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    variant_id = request.POST.get('variant_id')

    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product)

    cart_service = CartService(request.user)
    cart_service.add_item(product, quantity, variant)

    messages.success(request, f'{product.name} added to cart.')

    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = cart_service.get_cart()
        return JsonResponse({
            'success': True,
            'cart_count': cart.items_count if cart else 0,
            'message': f'{product.name} added to cart.'
        })

    return redirect('cart:view')


@login_required
@require_http_methods(["POST"])
def update_cart_view(request, item_id):
    """
    Update cart item quantity.
    """
    quantity = int(request.POST.get('quantity', 1))

    cart_service = CartService(request.user)
    cart_service.update_item(item_id, quantity)

    messages.success(request, 'Cart updated.')
    return redirect('cart:view')


@login_required
@require_http_methods(["POST"])
def remove_from_cart_view(request, item_id):
    """
    Remove item from cart.
    """
    cart_service = CartService(request.user)
    cart_service.remove_item(item_id)

    messages.success(request, 'Item removed from cart.')
    return redirect('cart:view')


@login_required
def clear_cart_view(request):
    """
    Clear entire cart.
    """
    cart_service = CartService(request.user)
    cart_service.clear_cart()

    messages.info(request, 'Cart cleared.')
    return redirect('cart:view')