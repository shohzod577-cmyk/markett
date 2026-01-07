"""
Product models for Market e-commerce platform.
Supports categories, multiple images, variants, and ratings.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Category(models.Model):
    """
    Hierarchical category system supporting nested categories.
    """

    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200, unique=True)
    description = models.TextField(_('description'), blank=True)

    # Hierarchy support
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True,
        verbose_name=_('parent category')
    )

    # Display
    image = models.ImageField(_('image'), upload_to='categories/', blank=True, null=True)
    icon = models.CharField(_('icon class'), max_length=100, blank=True, help_text='CSS icon class')

    # Ordering
    order = models.PositiveIntegerField(_('order'), default=0)

    # Status
    is_active = models.BooleanField(_('active'), default=True)

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def product_count(self):
        """Return number of active products in this category."""
        return self.products.filter(is_active=True).count()


class Product(models.Model):
    """
    Core Product model with comprehensive e-commerce features.
    """

    # Basic information
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    description = models.TextField(_('description'))
    short_description = models.CharField(_('short description'), max_length=500, blank=True)

    # Category
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name=_('category')
    )

    # Pricing (stored in base currency - UZS)
    price = models.DecimalField(
        _('price'),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    # Discount
    discount_percentage = models.DecimalField(
        _('discount percentage'),
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    # Inventory
    stock = models.PositiveIntegerField(_('stock quantity'), default=0)
    sku = models.CharField(_('SKU'), max_length=100, unique=True)

    # Product attributes
    brand = models.CharField(_('brand'), max_length=100, blank=True)
    weight = models.DecimalField(
        _('weight (kg)'),
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True
    )

    # SEO
    meta_title = models.CharField(_('meta title'), max_length=200, blank=True)
    meta_description = models.TextField(_('meta description'), blank=True)

    # Status
    is_active = models.BooleanField(_('active'), default=True)
    is_featured = models.BooleanField(_('featured'), default=False)

    # Statistics
    views_count = models.PositiveIntegerField(_('views'), default=0)
    sales_count = models.PositiveIntegerField(_('sales'), default=0)

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        """Calculate price after discount."""
        if self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price

    @property
    def is_in_stock(self):
        """Check if product is available."""
        return self.stock > 0

    @property
    def average_rating(self):
        """Calculate average rating from reviews."""
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

    @property
    def review_count(self):
        """Return total number of reviews."""
        return self.reviews.count()

    def increment_views(self):
        """Increment product view counter."""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class ProductImage(models.Model):
    """
    Product images with support for multiple images per product.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('product')
    )

    image = models.ImageField(_('image'), upload_to='products/')
    alt_text = models.CharField(_('alt text'), max_length=200, blank=True)
    is_primary = models.BooleanField(_('primary image'), default=False)
    order = models.PositiveIntegerField(_('order'), default=0)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        db_table = 'product_images'
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
        ordering = ['order', '-is_primary']

    def __str__(self):
        return f"Image for {self.product.name}"

    def save(self, *args, **kwargs):
        """Ensure only one primary image per product."""
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductVariant(models.Model):
    """
    Product variants for size, color, etc.
    Example: T-Shirt with sizes S, M, L, XL
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name=_('product')
    )

    name = models.CharField(_('variant name'), max_length=100, help_text='e.g., Size, Color')
    value = models.CharField(_('variant value'), max_length=100, help_text='e.g., Large, Red')

    # Price adjustment
    price_adjustment = models.DecimalField(
        _('price adjustment'),
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Additional price for this variant'
    )

    # Stock
    stock = models.PositiveIntegerField(_('stock'), default=0)
    sku_suffix = models.CharField(_('SKU suffix'), max_length=50, blank=True)

    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        db_table = 'product_variants'
        verbose_name = _('Product Variant')
        verbose_name_plural = _('Product Variants')
        unique_together = ['product', 'name', 'value']

    def __str__(self):
        return f"{self.product.name} - {self.name}:  {self.value}"