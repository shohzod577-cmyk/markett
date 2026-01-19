from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'sku', 'price', 'currency', 'is_active')
    search_fields = ('title', 'sku')
    list_filter = ('is_active', 'category')
    inlines = [ProductImageInline, ProductVariantInline]
