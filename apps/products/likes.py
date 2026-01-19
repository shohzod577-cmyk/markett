"""
Product like views for handling AJAX like/unlike actions.
"""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Product, ProductLike


@login_required
@require_POST
def toggle_like(request, product_id):
    """
    Toggle like status for a product.
    Returns JSON with like status and count.
    """
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    try:
        like = ProductLike.objects.get(product=product, user=request.user)
        like.delete()
        liked = False
        message = 'Product unliked'
    except ProductLike.DoesNotExist:
        ProductLike.objects.create(product=product, user=request.user)
        liked = True
        message = 'Product liked'
    
    likes_count = product.likes.count()
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'likes_count': likes_count,
        'message': message
    })


@login_required
def get_like_status(request, product_id):
    """
    Get like status for a product.
    """
    product = get_object_or_404(Product, id=product_id, is_active=True)
    liked = ProductLike.objects.filter(product=product, user=request.user).exists()
    likes_count = product.likes.count()
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'likes_count': likes_count
    })
