from django.shortcuts import render, get_object_or_404
from .models import Product
from django.core.paginator import Paginator


def product_list(request):
    qs = Product.objects.filter(is_active=True).order_by('-created_at')
    q = request.GET.get('q')
    if q:
        qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q)

    paginator = Paginator(qs, 12)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return render(request, 'products/product_list.html', {'products': items})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'products/product_detail.html', {'product': product})
