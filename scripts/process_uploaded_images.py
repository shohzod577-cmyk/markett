import os
import sys
import django
import shutil
from pathlib import Path
from difflib import SequenceMatcher

sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product, ProductImage

IMAGES_FOLDER = Path(__file__).resolve().parent.parent / 'rasimlar'

def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_best_match(filename, products):
    """Find the best matching product for a filename"""
    name_without_ext = Path(filename).stem.lower()
    
    import re
    clean_name = re.sub(r'[0-9_\-\(\)]', ' ', name_without_ext).strip()
    
    best_match = None
    best_score = 0
    
    for product in products:
        score = similarity(clean_name, product.name)
        
        if product.name.lower() in clean_name:
            score += 0.5
        
        keywords = {
            'non': ['bread', 'non', 'oq', 'qora', 'bulka'],
            'sut': ['milk', 'sut', 'qatiq', 'yogurt'],
            'gosht': ['meat', 'gosht', 'mol', 'qoy', 'tovuq', 'baliq', 'fish', 'chicken', 'beef', 'lamb'],
            'meva': ['fruit', 'meva', 'olma', 'apple', 'banan', 'banana', 'apelsin', 'orange', 'uzum', 'grape'],
            'sabzavot': ['vegetable', 'sabzi', 'pomidor', 'tomato', 'bodring', 'cucumber', 'qalampir', 'pepper'],
            'don': ['grain', 'guruch', 'rice', 'makaron', 'pasta', 'loviya', 'bean', 'noxat'],
            'taom': ['dish', 'osh', 'plov', 'lagmon', 'manti', 'somsa', 'shashlik', 'kabob', 'kebab', 'dumpling'],
            'ichimlik': ['drink', 'cola', 'pepsi', 'fanta', 'sprite', 'juice'],
            'shirinlik': ['cake', 'tort', 'sweet', 'candy', 'shirinlik'],
            'pishloq': ['cheese', 'pishloq'],
            'sariyog': ['butter', 'sariyog'],
            'tuxum': ['egg', 'tuxum'],
        }
        
        for key, words in keywords.items():
            if any(word in clean_name for word in words):
                if any(word in product.name.lower() for word in words):
                    score += 0.3
        
        if score > best_score:
            best_score = score
            best_match = product
    
    return best_match, best_score

def process_images():
    """Process all images in the rasimlar folder"""
    if not IMAGES_FOLDER.exists():
        print("❌ 'rasimlar' papkasi topilmadi!")
        return
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(IMAGES_FOLDER.glob(f'*{ext}'))
        image_files.extend(IMAGES_FOLDER.glob(f'*{ext.upper()}'))
    
    if not image_files:
        print("❌ 'rasimlar' papkasida rasm topilmadi!")
        print(f"📁 Rasmlarni shu papkaga qo'ying: {IMAGES_FOLDER}")
        return
    
    print("\n" + "="*60)
    print(f"RASIMLARNI TAHLIL QILISH VA JOYLASHTIRISH")
    print("="*60)
    print(f"Topilgan rasmlar: {len(image_files)} ta\n")
    
    products = list(Product.objects.all())
    processed = []
    skipped = []
    
    for img_file in image_files:
        print(f"📷 {img_file.name}")
        
        best_match, score = find_best_match(img_file.name, products)
        
        if best_match and score > 0.3:
            print(f"   ✓ Mos keldi: {best_match.name} (sifat: {score:.2f})")
            
            product_image = best_match.images.first()
            
            if product_image:
                dest_path = Path(product_image.image.path)
                
                try:
                    shutil.copy2(img_file, dest_path)
                    print(f"   ✓ Rasm yangilandi: {best_match.name}")
                    processed.append((img_file.name, best_match.name))
                except Exception as e:
                    print(f"   ❌ Xatolik: {str(e)}")
                    skipped.append((img_file.name, str(e)))
            else:
                print(f"   ⚠ Mahsulotda rasm yo'q: {best_match.name}")
                skipped.append((img_file.name, "ProductImage yo'q"))
        else:
            match_name = best_match.name if best_match else "Yo'q"
            print(f"   ⚠ Mos mahsulot topilmadi (eng yaxshi: {match_name}, sifat: {score:.2f})")
            print(f"      Qo'lda belgilang: {img_file.name}")
            skipped.append((img_file.name, "Mos mahsulot topilmadi"))
        
        print()
    
    print("="*60)
    print("NATIJA")
    print("="*60)
    print(f"Jami rasmlar: {len(image_files)}")
    print(f"Joylashtirилди: {len(processed)}")
    print(f"O'tkazib yuborildi: {len(skipped)}")
    
    if processed:
        print(f"\n✓ JOYLASHTRILGAN:")
        for img_name, product_name in processed:
            print(f"   {img_name} → {product_name}")
    
    if skipped:
        print(f"\n⚠ O'TKAZIB YUBORILGAN:")
        for img_name, reason in skipped:
            print(f"   {img_name} - {reason}")
    
    products_without_images = []
    for product in products:
        if not product.images.exists():
            products_without_images.append(product.name)
    
    if not products_without_images:
        print("\n" + "="*60)
        print("✅ BARCHA MAHSULOTLARDA RASM BOR!")
        print("="*60)
        
        response = input("\n'rasimlar' papkasini o'chirasizmi? (ha/yo'q): ")
        if response.lower() in ['ha', 'yes', 'y']:
            try:
                shutil.rmtree(IMAGES_FOLDER)
                print("✓ 'rasimlar' papkasi o'chirildi")
            except Exception as e:
                print(f"❌ O'chirib bo'lmadi: {str(e)}")
    else:
        print(f"\n⚠ Yana {len(products_without_images)} ta mahsulotda rasm yo'q:")
        for name in products_without_images[:10]:
            print(f"   - {name}")
    
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    process_images()
