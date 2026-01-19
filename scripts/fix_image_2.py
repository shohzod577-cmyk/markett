"""
Fix specific ProductImage ID 2
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import ProductImage

try:
    img = ProductImage.objects.get(id=2)
    print(f"Topildi: {img.product.name} - {img.image.name}")
    
    if img.image.storage.exists(img.image.name):
        print("✓ Fayl mavjud")
    else:
        print("✗ Fayl yo'q - o'chirilmoqda...")
        img.delete()
        print("✓ O'chirildi")
except ProductImage.DoesNotExist:
    print("ProductImage ID=2 topilmadi (allaqachon o'chirilgan)")
