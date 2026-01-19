from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=270, unique=True)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='UZS')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    is_active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        indexes = [
            models.Index(fields=['slug'], name='products_slug_idx'),
            models.Index(fields=['sku'], name='products_sku_idx'),
            models.Index(fields=['-created_at'], name='products_created_idx'),
        ]

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title

    @property
    def discount_percentage(self):
        return 0

    @property
    def discounted_price(self):
        return self.price

    @property
    def average_rating(self):
        try:
            return int(self.rating)
        except Exception:
            return 0

    @property
    def review_count(self):
        return 0

    @property
    def is_in_stock(self):
        variants = getattr(self, 'variants', None)
        if variants and variants.exists():
            return any(v.stock > 0 for v in variants.all())
        return True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:270]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('products:detail', args=[self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    alt = models.CharField(max_length=255, blank=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        db_table = 'product_images'

    def __str__(self):
        return f"Image for {self.product_id}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)

    class Meta:
        db_table = 'product_variants'
        unique_together = (('product', 'sku'),)

    def __str__(self):
        return f"{self.product.title} - {self.name}"
