"""
Script to add Coca-Cola product to the database.
Usage: python manage.py shell < scripts/add_coca_cola.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product, ProductImage, Category

category, created = Category.objects.get_or_create(
    slug='ichimliklar',
    defaults={
        'name': 'Ichimliklar',
        'description': 'Sovuq va issiq ichimliklar',
        'is_active': True,
        'order': 1
    }
)

if created:
    print(f"✓ Yangi kategoriya yaratildi: {category.name}")
else:
    print(f"✓ Kategoriya mavjud: {category.name}")

product, created = Product.objects.get_or_create(
    sku='COCA-COLA-330ML',
    defaults={
        'name': 'Coca-Cola',
        'slug': 'coca-cola-330ml',
        'description': 'Coca-Cola - dunyodagi eng mashhur gazlangan ichimlik. 330ml shisha idishda.',
        'short_description': 'Original Coca-Cola gazlangan ichimlik 330ml',
        'category': category,
        'price': 5000,
        'discount_percentage': 0,
        'stock': 100,
        'brand': 'Coca-Cola',
        'weight': 0.330,
        'is_active': True,
        'is_featured': True,
        'meta_title': 'Coca-Cola 330ml - Original ichimlik',
        'meta_description': 'Coca-Cola gazlangan ichimlik 330ml. Tez yetkazib berish va qulay narxlarda.',
    }
)

if created:
    print(f"✓ Yangi mahsulot yaratildi: {product.name}")
    
    product_image = ProductImage.objects.create(
        product=product,
        image='products/coca-cola.png',
        alt_text='Coca-Cola 330ml shisha',
        is_primary=True,
        order=0
    )
    print(f"✓ Mahsulot rasmi qo'shildi")
else:
    print(f"✓ Mahsulot allaqachon mavjud: {product.name}")

print("\n" + "="*50)
print("BAJARILDI!")
print("="*50)
print(f"\nMahsulot: {product.name}")
print(f"Narxi: {product.price:,.0f} so'm")
print(f"SKU: {product.sku}")
print(f"Kategoriya: {category.name}")
print(f"Omborda: {product.stock} dona")
print(f"\nMahsulotni ko'rish: /products/{product.slug}/")
