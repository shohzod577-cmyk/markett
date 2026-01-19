"""
Product catalog views.
"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Avg

from .models import Product, Category
from .filters import ProductFilter


def product_list_view(request):
    """
    Product listing with filtering and pagination.
    """
    products = Product.objects.filter(is_active=True).select_related('category')

    product_filter = ProductFilter(request.GET, queryset=products)
    products = product_filter.qs

    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )

    category_param = request.GET.get('category')
    if category_param:
        if category_param.isdigit():
            category = get_object_or_404(Category, id=int(category_param))
        else:
            category = get_object_or_404(Category, slug=category_param)
        products = products.filter(category=category)

    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'popular':
        products = products.order_by('-sales_count')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        products = products.order_by(sort_by)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filter': product_filter,
        'categories': Category.objects.filter(is_active=True, parent=None),
        'search_query': search_query,
    }

    return render(request, 'products/product_list.html', context)


def product_detail_view(request, slug):
    """
    Product detail view with reviews and related products.
    """
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('images', 'variants'),
        slug=slug,
        is_active=True
    )

    product.increment_views()

    reviews = product.reviews.filter(is_approved=True).select_related('user').order_by('-created_at')

    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    currency = request.session.get('currency', 'UZS')

    from core.services.currency import CurrencyService
    currency_service = CurrencyService()
    display_price = currency_service.get_display_price(product.discounted_price, currency)

    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'display_price': display_price,
    }

    return render(request, 'products/product_detail.html', context)


def category_list_view(request):
    """
    Display all categories.
    """
    categories = Category.objects.filter(is_active=True, parent=None).prefetch_related('children')

    context = {
        'categories': categories,
    }

    return render(request, 'products/category_list.html', context)