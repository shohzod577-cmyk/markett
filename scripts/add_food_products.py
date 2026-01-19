"""
Add food products from the image to the database
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Category, Product

categories_data = [
    {
        'name': 'Non mahsulotlari',
        'slug': 'non-mahsulotlari',
        'description': 'Non, bulka va boshqa non mahsulotlari',
        'order': 1
    },
    {
        'name': 'Sut mahsulotlari',
        'slug': 'sut-mahsulotlari',
        'description': 'Sut, qatiq, pishloq va boshqa sut mahsulotlari',
        'order': 2
    },
    {
        'name': 'Go\'sht va baliq',
        'slug': 'gosht-baliq',
        'description': 'Yangi go\'sht, tovuq go\'shti va baliq',
        'order': 3
    },
    {
        'name': 'Meva va sabzavotlar',
        'slug': 'meva-sabzavot',
        'description': 'Yangi meva va sabzavotlar',
        'order': 4
    },
    {
        'name': 'Donli mahsulotlar',
        'slug': 'donli-mahsulotlar',
        'description': 'Guruch, loviya, no\'xat va boshqa donlar',
        'order': 5
    },
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={
            'name': cat_data['name'],
            'description': cat_data['description'],
            'order': cat_data['order'],
            'is_active': True
        }
    )
    if created:
        print(f"✓ Kategoriya yaratildi: {category.name}")
    else:
        print(f"○ Kategoriya mavjud: {category.name}")

non = Category.objects.get(slug='non-mahsulotlari')
sut = Category.objects.get(slug='sut-mahsulotlari')
gosht = Category.objects.get(slug='gosht-baliq')
meva = Category.objects.get(slug='meva-sabzavot')
don = Category.objects.get(slug='donli-mahsulotlar')

products_data = [
    {
        'name': 'Oq non',
        'slug': 'oq-non',
        'category': non,
        'price': 3000,
        'stock': 100,
        'sku': 'NON-001',
        'description': 'Yangi pishirilgan oq non, yumshoq va mazali',
        'short_description': 'Yangi pishirilgan oq non',
    },
    {
        'name': 'Qora non',
        'slug': 'qora-non',
        'category': non,
        'price': 3500,
        'stock': 80,
        'sku': 'NON-002',
        'description': 'Butun donli qora non, foydali va to\'yimli',
        'short_description': 'Butun donli qora non',
    },
    {
        'name': 'Bulka',
        'slug': 'bulka',
        'category': non,
        'price': 2000,
        'stock': 150,
        'sku': 'NON-003',
        'description': 'Yumshoq va xushbo\'y bulka, nonushta uchun ajoyib',
        'short_description': 'Yumshoq bulka',
    },
    
    {
        'name': 'Sut (1 litr)',
        'slug': 'sut-1l',
        'category': sut,
        'price': 9000,
        'stock': 200,
        'sku': 'SUT-001',
        'description': 'Yangi sog\'ilgan sut, 100% tabiiy',
        'short_description': 'Tabiiy sut 1 litr',
        'weight': 1.0
    },
    {
        'name': 'Qatiq (500g)',
        'slug': 'qatiq-500g',
        'category': sut,
        'price': 8000,
        'stock': 150,
        'sku': 'SUT-002',
        'description': 'Uy qatiqi, tabiiy va mazali',
        'short_description': 'Uy qatiqi',
        'weight': 0.5
    },
    {
        'name': 'Pishloq (1kg)',
        'slug': 'pishloq-1kg',
        'category': sut,
        'price': 55000,
        'stock': 50,
        'sku': 'SUT-003',
        'description': 'Yumshoq pishloq, sendvich va salat uchun',
        'short_description': 'Yumshoq pishloq',
        'weight': 1.0
    },
    {
        'name': 'Sariyog\' (200g)',
        'slug': 'sariyog-200g',
        'category': sut,
        'price': 18000,
        'stock': 100,
        'sku': 'SUT-004',
        'description': '100% tabiiy sariyog\', yuqori sifatli',
        'short_description': 'Tabiiy sariyog\'',
        'weight': 0.2
    },
    
    {
        'name': 'Mol go\'shti (1kg)',
        'slug': 'mol-goshti-1kg',
        'category': gosht,
        'price': 85000,
        'stock': 30,
        'sku': 'GOSHT-001',
        'description': 'Yangi mol go\'shti, yumshoq qism',
        'short_description': 'Yangi mol go\'shti',
        'weight': 1.0
    },
    {
        'name': 'Tovuq go\'shti (1kg)',
        'slug': 'tovuq-goshti-1kg',
        'category': gosht,
        'price': 35000,
        'stock': 80,
        'sku': 'GOSHT-002',
        'description': 'Yangi tovuq go\'shti, oq go\'sht',
        'short_description': 'Tovuq go\'shti',
        'weight': 1.0
    },
    {
        'name': 'Baliq (1kg)',
        'slug': 'baliq-1kg',
        'category': gosht,
        'price': 45000,
        'stock': 40,
        'sku': 'GOSHT-003',
        'description': 'Yangi dengiz baliqi, omega-3 ga boy',
        'short_description': 'Yangi baliq',
        'weight': 1.0
    },
    {
        'name': 'Tuxum (10 dona)',
        'slug': 'tuxum-10',
        'category': gosht,
        'price': 15000,
        'stock': 200,
        'sku': 'GOSHT-004',
        'description': 'Yangi tovuq tuxumi, 10 donasi',
        'short_description': 'Tovuq tuxumi',
    },
    
    {
        'name': 'Pomidor (1kg)',
        'slug': 'pomidor-1kg',
        'category': meva,
        'price': 12000,
        'stock': 150,
        'sku': 'SABZAVOT-001',
        'description': 'Yangi qizil pomidor, mazali va suvli',
        'short_description': 'Yangi pomidor',
        'weight': 1.0
    },
    {
        'name': 'Sabzi (1kg)',
        'slug': 'sabzi-1kg',
        'category': meva,
        'price': 8000,
        'stock': 200,
        'sku': 'SABZAVOT-002',
        'description': 'Yangi sabzi, shirinroq nav',
        'short_description': 'Yangi sabzi',
        'weight': 1.0
    },
    {
        'name': 'Qalampir (1kg)',
        'slug': 'qalampir-1kg',
        'category': meva,
        'price': 15000,
        'stock': 100,
        'sku': 'SABZAVOT-003',
        'description': 'Qizil va yashil qalampir aralashmasi',
        'short_description': 'Rangli qalampir',
        'weight': 1.0
    },
    {
        'name': 'Bodring (1kg)',
        'slug': 'bodring-1kg',
        'category': meva,
        'price': 10000,
        'stock': 120,
        'sku': 'SABZAVOT-004',
        'description': 'Yangi bodring, salat uchun ajoyib',
        'short_description': 'Yangi bodring',
        'weight': 1.0
    },
    {
        'name': 'Banan (1kg)',
        'slug': 'banan-1kg',
        'category': meva,
        'price': 18000,
        'stock': 100,
        'sku': 'MEVA-001',
        'description': 'Pishgan banan, shirin va mazali',
        'short_description': 'Pishgan banan',
        'weight': 1.0
    },
    {
        'name': 'Apelsin (1kg)',
        'slug': 'apelsin-1kg',
        'category': meva,
        'price': 16000,
        'stock': 150,
        'sku': 'MEVA-002',
        'description': 'Suvli apelsin, vitamin C ga boy',
        'short_description': 'Suvli apelsin',
        'weight': 1.0
    },
    
    {
        'name': 'Guruch (1kg)',
        'slug': 'guruch-1kg',
        'category': don,
        'price': 12000,
        'stock': 300,
        'sku': 'DON-001',
        'description': 'Yuqori sifatli guruch, osh va palov uchun',
        'short_description': 'Sifatli guruch',
        'weight': 1.0
    },
    {
        'name': 'Loviya (1kg)',
        'slug': 'loviya-1kg',
        'category': don,
        'price': 15000,
        'stock': 200,
        'sku': 'DON-002',
        'description': 'Oq loviya, oqsil va tolaga boy',
        'short_description': 'Oq loviya',
        'weight': 1.0
    },
    {
        'name': 'No\'xat (1kg)',
        'slug': 'noxat-1kg',
        'category': don,
        'price': 18000,
        'stock': 150,
        'sku': 'DON-003',
        'description': 'Toza no\'xat, sho\'rva va osh uchun',
        'short_description': 'Toza no\'xat',
        'weight': 1.0
    },
    {
        'name': 'Makaron (500g)',
        'slug': 'makaron-500g',
        'category': don,
        'price': 8000,
        'stock': 250,
        'sku': 'DON-004',
        'description': 'Yuqori sifatli makaron, tez pishadi',
        'short_description': 'Makaron',
        'weight': 0.5
    },
]

print("\n" + "="*50)
print("MAHSULOTLARNI QO'SHISH BOSHLANDI")
print("="*50 + "\n")

for product_data in products_data:
    product, created = Product.objects.get_or_create(
        sku=product_data['sku'],
        defaults={
            'name': product_data['name'],
            'slug': product_data['slug'],
            'category': product_data['category'],
            'price': product_data['price'],
            'stock': product_data['stock'],
            'description': product_data['description'],
            'short_description': product_data['short_description'],
            'weight': product_data.get('weight', 0),
            'is_active': True,
            'is_featured': False,
        }
    )
    
    if created:
        print(f"✓ Qo'shildi: {product.name} - {product.price:,} so'm ({product.category.name})")
    else:
        print(f"○ Mavjud: {product.name}")

print("\n" + "="*50)
print(f"JAMI: {Product.objects.count()} ta mahsulot")
print(f"KATEGORIYALAR: {Category.objects.count()} ta")
print("="*50)
