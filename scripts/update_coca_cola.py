"""
Script to update Coca-Cola product.
Usage: python manage.py shell < scripts/update_coca_cola.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product, Category

try:
    product = Product.objects.get(sku='COCA-COLA-330ML')
    
    product.price = 5000
    product.stock = 150
    product.is_active = True
    product.is_featured = True
    product.save()
    
    print(f"✓ Mahsulot yangilandi: {product.name}")
    print(f"  - Yangi narx: {product.price:,.0f} so'm")
    print(f"  - Kategoriya: {product.category.name}")
    print(f"  - Omborda: {product.stock} dona")
    print(f"  - Status: {'Faol' if product.is_active else 'Nofaol'}")
    
except Product.DoesNotExist:
    print("❌ Coca-Cola mahsuloti topilmadi!")
except Exception as e:
    print(f"❌ Xatolik: {e}")
