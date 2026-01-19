"""
List all products without images
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product

products_without_images = Product.objects.filter(images__isnull=True).distinct()

print("\n" + "="*60)
print(f"RASMI YO'Q MAHSULOTLAR: {products_without_images.count()} ta")
print("="*60 + "\n")

if products_without_images.exists():
    for i, product in enumerate(products_without_images, 1):
        print(f"{i}. {product.name} (Kategoriya: {product.category.name})")
else:
    print("✅ Barcha mahsulotlarda rasm bor!")

print("\n" + "="*60)
print(f"Jami mahsulotlar: {Product.objects.count()}")
print(f"Rasm bilan: {Product.objects.filter(images__isnull=False).distinct().count()}")
print(f"Rasm yo'q: {products_without_images.count()}")
print("="*60)
