"""
Home view for Market platform.
"""
from django.shortcuts import render
from apps.products.models import Product, Category


def home_view(request):
    """
    Home page view with featured products and categories.
    """
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('category').prefetch_related('images')[:8]

    categories = Category.objects.filter(
        is_active=True,
        parent=None
    )[: 12]

    context = {
        'featured_products': featured_products,
        'categories': categories,
    }

    return render(request, 'home.html', context)