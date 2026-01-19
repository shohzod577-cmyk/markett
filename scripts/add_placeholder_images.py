"""
Add placeholder images for products without images
"""
import os
import sys
import django
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files.uploadedfile import InMemoryUploadedFile
from apps.products.models import Product, ProductImage

def create_placeholder_image(product_name, width=800, height=800):
    """Create a placeholder image with product name."""
    img = Image.new('RGB', (width, height), color='#f0f0f0')
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([(10, 10), (width-10, height-10)], outline='#cccccc', width=5)
    
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    text = product_name
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((width - text_width) // 2, (height - text_height) // 2)
    
    draw.text(position, text, fill='#666666', font=font)
    
    watermark = "Markett.uz"
    try:
        small_font = ImageFont.truetype("arial.ttf", 30)
    except:
        small_font = font
    
    draw.text((30, height - 60), watermark, fill='#999999', font=small_font)
    
    return img

def save_image_to_product(product, img):
    """Save PIL image to product."""
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=90)
    img_io.seek(0)
    
    img_file = InMemoryUploadedFile(
        img_io, None, f'{product.slug}.jpg', 'image/jpeg',
        img_io.getbuffer().nbytes, None
    )
    
    product_image = ProductImage.objects.create(
        product=product,
        image=img_file,
        alt_text=product.name,
        is_primary=True,
        order=0
    )
    
    return product_image

products_without_images = Product.objects.filter(images__isnull=True).distinct()

print("\n" + "="*60)
print(f"RASM YO'Q MAHSULOTLAR: {products_without_images.count()} ta")
print("="*60 + "\n")

for product in products_without_images:
    print(f"Rasm yaratilmoqda: {product.name}...")
    
    img = create_placeholder_image(product.name)
    
    try:
        product_image = save_image_to_product(product, img)
        print(f"✓ Rasm qo'shildi: {product.name}")
    except Exception as e:
        print(f"✗ Xatolik: {product.name} - {e}")

print("\n" + "="*60)
print("RASM QO'SHISH TUGADI")
print("="*60)

total_products = Product.objects.count()
products_with_images = Product.objects.filter(images__isnull=False).distinct().count()
products_without_images = total_products - products_with_images

print(f"\nJami mahsulotlar: {total_products}")
print(f"Rasm bilan: {products_with_images}")
print(f"Rasm yo'q: {products_without_images}")
