"""
Add prepared food/meals category and products
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Category, Product

meals_category, created = Category.objects.get_or_create(
    slug='taomlar',
    defaults={
        'name': 'Taomlar',
        'description': 'Tayyor taomlar va milliy taomlar',
        'order': 6,
        'is_active': True
    }
)

if created:
    print(f"✓ Kategoriya yaratildi: {meals_category.name}")
else:
    print(f"○ Kategoriya mavjud: {meals_category.name}")

meals_data = [
    {
        'name': 'Osh',
        'slug': 'osh',
        'price': 25000,
        'stock': 50,
        'sku': 'TAOM-001',
        'description': 'An\'anaviy o\'zbek oshi, guruch va go\'sht bilan',
        'short_description': 'O\'zbek oshi',
        'weight': 0.5
    },
    {
        'name': 'Lag\'mon',
        'slug': 'lagmon',
        'price': 22000,
        'stock': 40,
        'sku': 'TAOM-002',
        'description': 'Uyg\'ur lag\'moni, go\'sht va sabzavotlar bilan',
        'short_description': 'Uyg\'ur lag\'moni',
        'weight': 0.5
    },
    {
        'name': 'Manti',
        'slug': 'manti',
        'price': 20000,
        'stock': 60,
        'sku': 'TAOM-003',
        'description': 'Bug\'da pishirilgan manti, go\'sht plombirli',
        'short_description': 'Go\'shtli manti',
        'weight': 0.4
    },
    {
        'name': 'Somsa',
        'slug': 'somsa',
        'price': 5000,
        'stock': 100,
        'sku': 'TAOM-004',
        'description': 'Tandir somsasi, go\'sht va piyoz bilan',
        'short_description': 'Tandir somsasi',
        'weight': 0.15
    },
    {
        'name': 'Sho\'rva',
        'slug': 'shorva',
        'price': 15000,
        'stock': 40,
        'sku': 'TAOM-005',
        'description': 'Issiq sho\'rva, sabzavot va go\'sht bilan',
        'short_description': 'Go\'shtli sho\'rva',
        'weight': 0.4
    },
    {
        'name': 'Mastava',
        'slug': 'mastava',
        'price': 18000,
        'stock': 35,
        'sku': 'TAOM-006',
        'description': 'Mastava - guruch va go\'shtdan tayyorlangan sho\'rva',
        'short_description': 'Mastava sho\'rva',
        'weight': 0.4
    },
    {
        'name': 'Dimlama',
        'slug': 'dimlama',
        'price': 30000,
        'stock': 30,
        'sku': 'TAOM-007',
        'description': 'Go\'sht va sabzavotlardan tayyorlangan dimlama',
        'short_description': 'Dimlama',
        'weight': 0.6
    },
    {
        'name': 'Chuchvara',
        'slug': 'chuchvara',
        'price': 18000,
        'stock': 50,
        'sku': 'TAOM-008',
        'description': 'Kichik chuchvara sho\'rvasi',
        'short_description': 'Chuchvara',
        'weight': 0.4
    },
    {
        'name': 'No\'xat sho\'rva',
        'slug': 'noxat-shorva',
        'price': 12000,
        'stock': 45,
        'sku': 'TAOM-009',
        'description': 'No\'xatdan tayyorlangan sho\'rva',
        'short_description': 'No\'xat sho\'rva',
        'weight': 0.4
    },
    {
        'name': 'Qozon kabob',
        'slug': 'qozon-kabob',
        'price': 35000,
        'stock': 25,
        'sku': 'TAOM-010',
        'description': 'Qozonda pishirilgan kabob, sabzavotlar bilan',
        'short_description': 'Qozon kabob',
        'weight': 0.5
    },
    {
        'name': 'Shashlik',
        'slug': 'shashlik',
        'price': 40000,
        'stock': 40,
        'sku': 'TAOM-011',
        'description': 'O\'tda pishirilgan shashlik, 1kg',
        'short_description': 'Shashlik',
        'weight': 1.0
    },
    {
        'name': 'No\'xat osh',
        'slug': 'noxat-osh',
        'price': 20000,
        'stock': 35,
        'sku': 'TAOM-012',
        'description': 'No\'xat va guruchdan tayyorlangan osh',
        'short_description': 'No\'xat osh',
        'weight': 0.5
    },
    {
        'name': 'Barak',
        'slug': 'barak',
        'price': 22000,
        'stock': 30,
        'sku': 'TAOM-013',
        'description': 'Qovurilgan barak, go\'sht plombirli',
        'short_description': 'Go\'shtli barak',
        'weight': 0.4
    },
    {
        'name': 'Tandir kabob',
        'slug': 'tandir-kabob',
        'price': 38000,
        'stock': 20,
        'sku': 'TAOM-014',
        'description': 'Tandirda pishirilgan kabob',
        'short_description': 'Tandir kabob',
        'weight': 0.6
    },
    {
        'name': 'Non kabob',
        'slug': 'non-kabob',
        'price': 25000,
        'stock': 40,
        'sku': 'TAOM-015',
        'description': 'Non ichida kabob, sabzavotlar bilan',
        'short_description': 'Non kabob',
        'weight': 0.4
    },
]

print("\n" + "="*60)
print("TAOMLARNI QO'SHISH BOSHLANDI")
print("="*60 + "\n")

for meal_data in meals_data:
    product, created = Product.objects.get_or_create(
        sku=meal_data['sku'],
        defaults={
            'name': meal_data['name'],
            'slug': meal_data['slug'],
            'category': meals_category,
            'price': meal_data['price'],
            'stock': meal_data['stock'],
            'description': meal_data['description'],
            'short_description': meal_data['short_description'],
            'weight': meal_data['weight'],
            'is_active': True,
            'is_featured': True,
        }
    )
    
    if created:
        print(f"✓ Qo'shildi: {product.name} - {product.price:,} so'm")
    else:
        print(f"○ Mavjud: {product.name}")

print("\n" + "="*60)
print(f"TAOMLAR: {Product.objects.filter(category=meals_category).count()} ta")
print(f"JAMI MAHSULOTLAR: {Product.objects.count()} ta")
print(f"JAMI KATEGORIYALAR: {Category.objects.count()} ta")
print("="*60)
