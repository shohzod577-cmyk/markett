from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse

from apps.products.models import Product, ProductVariant
from .models import Cart, CartItem


def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_detail(request):
    cart = _get_or_create_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


def cart_add(request):
    product_id = request.POST.get('product_id')
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))

    product = get_object_or_404(Product, pk=product_id)
    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, pk=variant_id)

    cart = _get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, variant=variant)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    if request.is_ajax() or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'total_items': cart.total_items, 'subtotal': cart.subtotal})

    return redirect('cart:detail')


def cart_update(request, item_id):
    cart = _get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))
    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()
    return redirect('cart:detail')


def cart_remove(request, item_id):
    cart = _get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    return redirect('cart:detail')
