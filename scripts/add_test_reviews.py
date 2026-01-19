"""
Add test reviews for products
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product
from apps.reviews.models import Review
from apps.users.models import User

user, created = User.objects.get_or_create(
    email='test@example.com',
    defaults={
        'first_name': 'Test',
        'last_name': 'User',
    }
)
if created:
    user.set_password('test123')
    user.save()
    print(f"Created test user: {user.email}")

try:
    product = Product.objects.get(slug='tort')
    print(f"Found product: {product.name}")
    
    reviews_data = [
        {
            'rating': 5,
            'title': 'Ajoyib tort!',
            'comment': 'Bu tortni juda yoqtirdim. Ta\'mi juda mazali va sifati a\'lo. Hammaga tavsiya qilaman!',
        },
        {
            'rating': 4,
            'title': 'Yaxshi mahsulot',
            'comment': 'Umuman olganda yaxshi tort. Narxi ham o\'rtacha. Lekin biroz shirin.',
        },
        {
            'rating': 5,
            'title': 'Eng yaxshi tort',
            'comment': 'Bu yerdan doim tort olaman. Sifati doim bir xil va ta\'mi a\'lo!',
        },
    ]
    
    for review_data in reviews_data:
        review, created = Review.objects.get_or_create(
            product=product,
            user=user,
            rating=review_data['rating'],
            defaults={
                'title': review_data['title'],
                'comment': review_data['comment'],
                'is_approved': True,
                'is_verified_purchase': True,
            }
        )
        if created:
            print(f"✓ Added review: {review.title} ({review.rating} stars)")
        else:
            print(f"✗ Review already exists: {review.title}")
    
    print(f"\n📊 Average rating: {product.average_rating}/5")
    print(f"📝 Total reviews: {product.review_count}")
    
except Product.DoesNotExist:
    print("❌ Product 'tort' not found")
