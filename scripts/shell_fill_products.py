import os
from apps.products.models import Product, Category, ProductImage
from django.core.files import File
from django.utils.text import slugify
import random

media_dir = 'media/'
category = Category.objects.first() or Category.objects.create(name='Boshqa', slug='boshqa')

for filename in os.listdir(media_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        name = os.path.splitext(filename)[0]
        image_path = os.path.join(media_dir, filename)
        description = f"{name} mahsuloti. Bu mahsulot avtomatik yuklandi."
        short_description = f"{name} qisqacha tavsifi."
        price = round(random.uniform(10000, 100000), 2)
        sku = slugify(name)[:10] + str(random.randint(1000, 9999))
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
