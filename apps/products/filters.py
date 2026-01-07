"""
Product filtering using django-filter.
"""
import django_filters
from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    """
    Filter products by various criteria.
    """
    name = django_filters.CharFilter(lookup_expr='icontains', label='Product Name')

    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max Price')

    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.filter(is_active=True),
        label='Category'
    )

    brand = django_filters.CharFilter(lookup_expr='iexact', label='Brand')

    in_stock = django_filters.BooleanFilter(
        method='filter_in_stock',
        label='In Stock Only'
    )

    on_sale = django_filters.BooleanFilter(
        method='filter_on_sale',
        label='On Sale'
    )

    class Meta:
        model = Product
        fields = ['category', 'brand']

    def filter_in_stock(self, queryset, name, value):
        """Filter products that are in stock."""
        if value:
            return queryset.filter(stock__gt=0)
        return queryset

    def filter_on_sale(self, queryset, name, value):
        """Filter products with active discounts."""
        if value:
            return queryset.filter(discount_percentage__gt=0)
        return queryset