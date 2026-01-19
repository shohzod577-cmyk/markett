from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.products.models import Category, Product, ProductVariant


class Command(BaseCommand):
    help = 'Seed database with sample categories and products'

    def add_arguments(self, parser):
        parser.add_argument('--count-per-category', type=int, default=5, help='Products per category')

    def handle(self, *args, **options):
        count = options.get('count_per_category') or options.get('count-per-category') or 5

        categories = [
            'Electronics', 'Home & Kitchen', 'Books', 'Clothing', 'Beauty',
            'Sports', 'Toys', 'Groceries'
        ]

        created = 0
        for cat_name in categories:
            cat_slug = slugify(cat_name)
            category, _ = Category.objects.get_or_create(name=cat_name, slug=cat_slug)

            for i in range(1, count + 1):
                title = f"{cat_name} Sample {i}"
                slug = slugify(f"{title}-{i}")
                sku = f"{cat_slug[:3].upper()}-{i:03d}"
                product, created_flag = Product.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'title': title,
                        'sku': sku,
                        'description': f'Sample product {title} for category {cat_name}.',
                        'price': 100 + i * 10,
                        'currency': 'UZS',
                        'category': category,
                    }
                )
                if created_flag and (i % 3 == 0):
                    ProductVariant.objects.create(product=product, name='Default', sku=f"{sku}-V1", price=product.price, stock=10)

                if created_flag:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f'Created/ensured categories and {created} products.'))
