"""
Script to update Ichimliklar category image.
Usage: python manage.py shell < scripts/update_category_image.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Category

try:
    category = Category.objects.get(slug='ichimliklar')
    
    category.image = 'categories/drinks-collection.jpg'
    category.description = 'Turli xil ichimliklar: gazlangan, sharbatlar, mineralli suvlar va boshqalar'
    category.is_active = True
    category.save()
    
    print(f"✓ Kategoriya yangilandi: {category.name}")
    print(f"  - Rasm: {category.image}")
    print(f"  - Tavsif: {category.description}")
    
except Category.DoesNotExist:
    print("❌ Ichimliklar kategoriyasi topilmadi!")
except Exception as e:
    print(f"❌ Xatolik: {e}")
