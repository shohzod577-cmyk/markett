import os
import sys
import django
import requests
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product, ProductImage

SEARCH_TERMS = {
    'pishloq': 'cheese',
    'sariyog': 'butter',
    'sut': 'milk bottle',
    'qatiq': 'yogurt',
    
    'oq non': 'white bread loaf',
    'qora non': 'brown bread',
    'lavash': 'flatbread pita',
    
    'mol go\'shti': 'beef meat',
    'qo\'y go\'shti': 'lamb meat',
    'tovuq go\'shti': 'chicken meat',
    'baliq': 'fresh fish',
    
    'olma': 'red apple',
    'banan': 'banana',
    'apelsin': 'orange fruit',
    'uzum': 'grapes',
    'kartoshka': 'potato',
    'piyoz': 'onion',
    
    'guruch': 'rice grain',
    'makaron': 'pasta',
    'un': 'flour bag',
    'loviya': 'beans',
    
    'osh': 'uzbek plov rice',
    'lag\'mon': 'lagman noodles',
    'manti': 'dumplings steamed',
    'somsa': 'samosa pastry',
    'shashlik': 'kebab skewers',
    'dimlama': 'vegetable stew',
    'norin': 'noodle dish',
    'mastava': 'rice soup',
    'chuchvara': 'small dumplings',
    'qozon kabob': 'fried meat',
    'tandir kabob': 'tandoor meat',
    'palov': 'pilaf rice',
    'shurva': 'meat soup',
    'salat': 'fresh salad',
    'non kabob': 'bread kebab',
    
    'coca-cola': 'coca cola bottle',
    'pepsi': 'pepsi bottle',
    'fanta': 'fanta orange',
    'sprite': 'sprite bottle',
    
    'tort': 'chocolate cake',
    'shirinlik': 'sweets candy',
}

def download_image_from_unsplash(search_term, save_path):
    """Download image from Picsum (Lorem Picsum)"""
    url = f"https://picsum.photos/800/800"
    
    try:
        print(f"   Yuklanmoqda: {search_term}...")
        response = requests.get(url, timeout=15, allow_redirects=True)
        
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"   ❌ Xato: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Xatolik: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("HAQIQIY RASMLARNI YUKLAB OLISH")
    print("="*60 + "\n")
    
    products = Product.objects.all()
    total = products.count()
    success_count = 0
    failed = []
    
    for idx, product in enumerate(products, 1):
        product_name = product.name.lower()
        
        search_term = SEARCH_TERMS.get(product_name, product_name)
        
        print(f"{idx}/{total}. {product.name}...")
        
        product_image = product.images.first()
        
        if product_image and product_image.image:
            image_path = product_image.image.path
            
            if download_image_from_unsplash(search_term, image_path):
                print(f"   ✓ Rasm yangilandi")
                success_count += 1
            else:
                print(f"   ✗ Yuklab bo'lmadi")
                failed.append(product.name)
        else:
            print(f"   ⚠ Rasm yo'q")
            failed.append(product.name)
        
        time.sleep(1)
    
    print("\n" + "="*60)
    print("NATIJA")
    print("="*60)
    print(f"Jami: {total}")
    print(f"Muvaffaqiyatli: {success_count}")
    print(f"Xato: {len(failed)}")
    
    if failed:
        print(f"\nXato bo'lgan mahsulotlar:")
        for name in failed:
            print(f"  - {name}")
    
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
