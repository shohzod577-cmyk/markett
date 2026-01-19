"""
Fix Coca-Cola product image issue
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product, ProductImage
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

try:
    coca_cola = Product.objects.get(sku='COCA-COLA-330ML')
    print(f"Mahsulot topildi: {coca_cola.name}")
    
    existing_images = coca_cola.images.all()
    print(f"Mavjud rasmlar: {existing_images.count()} ta")
    
    for img in existing_images:
        print(f"  - {img.image.name}")
        if not os.path.exists(img.image.path):
            print(f"    ✗ Fayl mavjud emas: {img.image.path}")
            print(f"    Rasmni o'chirish...")
            img.delete()
    
    if coca_cola.images.count() == 0:
        print("\nPlaceholder rasm yaratilmoqda...")
        
        img = Image.new('RGB', (800, 800), color='#E53935')
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([(10, 10), (790, 790)], outline='#B71C1C', width=8)
        
        try:
            font_large = ImageFont.truetype("arial.ttf", 80)
            font_small = ImageFont.truetype("arial.ttf", 40)
        except:
            font_large = ImageFont.load_default()
            font_small = font_large
        
        text = "Coca-Cola"
        bbox = draw.textbbox((0, 0), text, font=font_large)
        text_width = bbox[2] - bbox[0]
        position = ((800 - text_width) // 2, 300)
        draw.text(position, text, fill='white', font=font_large)
        
        subtitle = "330ml"
        bbox2 = draw.textbbox((0, 0), subtitle, font=font_small)
        text_width2 = bbox2[2] - bbox2[0]
        position2 = ((800 - text_width2) // 2, 400)
        draw.text(position2, subtitle, fill='white', font=font_small)
        
        draw.text((30, 740), "Markett.uz", fill='#FFCDD2', font=font_small)
        
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=90)
        img_io.seek(0)
        
        img_file = InMemoryUploadedFile(
            img_io, None, 'coca-cola.jpg', 'image/jpeg',
            img_io.getbuffer().nbytes, None
        )
        
        product_image = ProductImage.objects.create(
            product=coca_cola,
            image=img_file,
            alt_text='Coca-Cola 330ml',
            is_primary=True,
            order=0
        )
        
        print(f"✓ Yangi rasm yaratildi: {product_image.image.name}")
    
    print(f"\n✅ Coca-Cola mahsuloti tuzatildi!")
    print(f"Jami rasmlar: {coca_cola.images.count()} ta")
    
except Product.DoesNotExist:
    print("❌ Coca-Cola mahsuloti topilmadi")
