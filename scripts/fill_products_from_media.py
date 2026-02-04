# Faqat random id ko‘rinishidagi mahsulotlarni o‘chirish funksiyasi
import re
from apps.products.models import Product
def is_random_name(name):
    # 32 ta harf/sonli yoki shunga o‘xshash nomlar (UUID, hash)
    return bool(re.fullmatch(r'[a-f0-9]{16,}', name.replace(' ', '').lower()))

deleted_count = 0
for product in Product.objects.all():
    if is_random_name(product.name):
        product.delete()
        deleted_count += 1
print(f'{deleted_count} ta noto‘g‘ri nomli mahsulot o‘chirildi.')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

counter = 1
category_images = {}
# Avval har bir kategoriya uchun mos rasmni aniqlab olamiz
for filename in os.listdir(media_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        human_name = humanize_filename(filename)
        category_name = human_name.split()[0] if human_name else 'Boshqa'
        # Har bir kategoriya uchun birinchi uchragan rasmni saqlaymiz
        if category_name not in category_images:
            category_images[category_name] = filename

for filename in os.listdir(media_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        image_path = os.path.join(media_dir, filename)
        human_name = humanize_filename(filename)
        category_name = human_name.split()[0] if human_name else 'Boshqa'
        # Kategoriya uchun rasm fayli
        category_image_filename = category_images.get(category_name)
        category_image_path = os.path.join(media_dir, category_image_filename) if category_image_filename else None
        # Kategoriya yaratish yoki olish
        from django.core.files import File as DjangoFile
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'slug': slugify(category_name)}
        )
        # Agar kategoriya yangi yaratilgan bo‘lsa va rasm bor bo‘lsa, image maydoniga rasm biriktiramiz
        if created and category_image_path and os.path.exists(category_image_path):
            with open(category_image_path, 'rb') as cat_img_file:
                category.image.save(category_image_filename, DjangoFile(cat_img_file), save=True)
        description = f"{human_name} mahsuloti. Bu mahsulot avtomatik yuklandi."
        short_description = f"{human_name} qisqacha tavsifi."
        price = get_random_price()
        slug = f"{slugify(human_name)}-{counter}"
        sku = get_random_sku(human_name)
        with open(image_path, 'rb') as img_file:
            product = Product.objects.create(
                name=human_name,
                slug=slug,
                description=description,
                short_description=short_description,
                category=category,
                price=price,
                sku=sku,
                is_active=True,
                is_featured=True,
                stock=100,
            )
            ProductImage.objects.create(product=product, image=DjangoFile(img_file), is_primary=True)
            print(f"{human_name} mahsuloti va rasmi yaratildi.")
        counter += 1
from django.core.files import File

media_dir = 'media/products/'

category, _ = Category.objects.get_or_create(
    name='Avtomatik Mahsulotlar',
    defaults={'slug': slugify('Avtomatik Mahsulotlar')}
)
def get_random_price():
    return round(random.uniform(10000, 100000), 2)

def get_random_sku(name):
    return slugify(name)[:10] + str(random.randint(1000, 9999))

import re
# Barcha eski mahsulotlarni o‘chirish
Product.objects.all().delete()
print('Barcha eski mahsulotlar o‘chirildi!')

def humanize_filename(filename):
    name = os.path.splitext(filename)[0]
    # Underscore, tire va nuqtalarni bo‘shliqqa almashtirish
    name = re.sub(r'[_\-.]+', ' ', name)
    # Har bir so‘zni bosh harf bilan
    name = ' '.join([w.capitalize() for w in name.split()])
    return name if name.strip() else 'Mahsulot'

counter = 1
for filename in os.listdir(media_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        image_path = os.path.join(media_dir, filename)
        human_name = humanize_filename(filename)
        # Kategoriya nomi birinchi so‘z (masalan, "Coca Cola 1l" → "Coca")
        category_name = human_name.split()[0] if human_name else 'Boshqa'
        # Kategoriya yaratish yoki olish
        category, _ = Category.objects.get_or_create(
            name=category_name,
            defaults={'slug': slugify(category_name)}
        )
        description = f"{human_name} mahsuloti. Bu mahsulot avtomatik yuklandi."
        short_description = f"{human_name} qisqacha tavsifi."
        price = get_random_price()
        # Slug har doim noyob bo‘lishi uchun counter qo‘shiladi
        slug = f"{slugify(human_name)}-{counter}"
        sku = get_random_sku(human_name)
        with open(image_path, 'rb') as img_file:
            product = Product.objects.create(
                name=human_name,
                slug=slug,
                description=description,
                short_description=short_description,
                category=category,
                price=price,
                sku=sku,
                is_active=True,
                is_featured=True,
                stock=100,
            )
            ProductImage.objects.create(product=product, image=File(img_file), is_primary=True)
            print(f"{human_name} mahsuloti va rasmi yaratildi.")
        counter += 1

for filename in os.listdir(media_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        name = os.path.splitext(filename)[0]
        image_path = os.path.join(media_dir, filename)
        description = f"{name} mahsuloti. Bu mahsulot avtomatik yuklandi."
        short_description = f"{name} qisqacha tavsifi."
        price = get_random_price()
        sku = get_random_sku(name)
        with open(image_path, 'rb') as img_file:
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': description,
                    'short_description': short_description,
                    'category': category,
                    'price': price,
                    'sku': sku,
                    'is_active': True,
                }
            )
            if created:
                ProductImage.objects.create(product=product, image=File(img_file), is_primary=True)
                print(f"{name} mahsuloti va rasmi yaratildi.")
            else:
                print(f"{name} mahsuloti mavjud.")
