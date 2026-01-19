"""Quick rating view"""
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.products.models import Product
from .models import ProductRating


@login_required
def rate_product_view(request, product_id):
    """
    Quick rating - user can rate product with stars (AJAX).
    """
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = int(request.POST.get('rating', 0))
        
        if rating < 1 or rating > 5:
            return JsonResponse({'success': False, 'error': 'Invalid rating'})
        
        product_rating, created = ProductRating.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating}
        )
        
        return JsonResponse({
            'success': True,
            'rating': rating,
            'average_rating': product.average_rating,
            'message': 'Rahmat! Sizning bahoyingiz qabul qilindi.' if created else 'Bahoyingiz yangilandi.'
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
