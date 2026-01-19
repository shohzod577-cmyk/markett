"""
Clean up ProductImage records with missing files
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import ProductImage

print("\n" + "="*60)
print("NOTO'G'RI RASMLARNI TOZALASH")
print("="*60 + "\n")

all_images = ProductImage.objects.all()
print(f"Jami rasmlar: {all_images.count()} ta\n")

deleted_count = 0
fixed_count = 0

for img in all_images:
    try:
        if not img.image.storage.exists(img.image.name):
            print(f"✗ Fayl yo'q: {img.product.name} - {img.image.name}")
            img.delete()
            deleted_count += 1
        else:
            _ = img.image.size
            fixed_count += 1
    except Exception as e:
        print(f"✗ Xatolik: {img.product.name} - {e}")
        img.delete()
        deleted_count += 1

print("\n" + "="*60)
print(f"Tozalandi: {deleted_count} ta")
print(f"To'g'ri: {fixed_count} ta")
print(f"Qolgan: {ProductImage.objects.count()} ta")
print("="*60)
