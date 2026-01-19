"""
Admin configuration for Products app.
Provides comprehensive interface for managing products, categories, images, and variants.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import Category, Product, ProductImage, ProductVariant


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images."""
    model = ProductImage
    extra = 1
    fields = ['image', 'image_preview', 'alt_text', 'is_primary', 'order']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        """Display image thumbnail in admin."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px; object-fit: contain; border: 1px solid #ddd; border-radius: 5px; padding: 5px;" />', 
                obj.image.url
            )
        return format_html('<span style="color: #999;">Rasm yuklanmagan</span>')
    image_preview.short_description = _('Preview')


class ProductVariantInline(admin.TabularInline):
    """Inline admin for product variants."""
    model = ProductVariant
    extra = 1
    fields = ['name', 'value', 'price_adjustment', 'stock', 'sku_suffix', 'is_active']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for product categories."""
    list_display = ['name', 'image_preview', 'parent', 'product_count_display', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        (_('Display'), {
            'fields': ('image', 'image_preview_large', 'icon', 'order'),
            'description': 'Kategoriya rasmini yuklang. Rasm kategoriyalar ro\'yxatida ko\'rinadi.'
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ['image_preview_large']
    
    def image_preview(self, obj):
        """Display small image thumbnail in list."""
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 5px;" />', obj.image.url)
        return format_html('<span style="color: #999;">Rasm yo\'q</span>')
    image_preview.short_description = _('Rasm')
    
    def image_preview_large(self, obj):
        """Display large image preview in edit form."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 400px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" /><br><small style="color: #666;">Joriy rasm</small>',
                obj.image.url
            )
        return format_html('<span style="color: #999; font-style: italic;">Hozircha rasm yuklanmagan</span>')
    image_preview_large.short_description = _('Rasm ko\'rinishi')
    
    def product_count_display(self, obj):
        """Display number of products in category."""
        count = obj.product_count
        url = reverse('admin:products_product_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">{} mahsulot</a>', url, count)
    product_count_display.short_description = _('Products')
    
    actions = ['activate_categories', 'deactivate_categories']
    
    def activate_categories(self, request, queryset):
        """Activate selected categories."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} ta kategoriya faollashtirildi.')
    activate_categories.short_description = _('Activate selected categories')
    
    def deactivate_categories(self, request, queryset):
        """Deactivate selected categories."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} ta kategoriya o\'chirildi.')
    deactivate_categories.short_description = _('Deactivate selected categories')
    
    def has_delete_permission(self, request, obj=None):
        """Allow admins to delete categories."""
        return request.user.is_superuser or request.user.is_staff


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for products with full CRUD functionality."""
    list_display = [
        'product_image_preview',
        'name', 
        'category', 
        'price_display',
        'discounted_price_display',
        'stock_status',
        'change_image_link',
        'is_featured',
        'is_active', 
        'views_count',
        'sales_count',
        'created_at'
    ]
    list_filter = [
        'is_active', 
        'is_featured', 
        'category',
        'created_at',
        'brand'
    ]
    search_fields = ['name', 'sku', 'description', 'brand']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_featured']
    date_hierarchy = 'created_at'
    
    def product_image_preview(self, obj):
        """Display product's primary image in list."""
        primary_image = obj.images.filter(is_primary=True).first()
        if not primary_image:
            primary_image = obj.images.first()
        
        if primary_image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 5px; border: 1px solid #ddd;" /></a>',
                primary_image.image.url,
                primary_image.image.url
            )
        return format_html('<span style="color: #999;">Rasm yo\'q</span>')
    product_image_preview.short_description = _('Rasm')
    
    def change_image_link(self, obj):
        """Display link to change product image."""
        primary_image = obj.images.filter(is_primary=True).first()
        if not primary_image:
            primary_image = obj.images.first()
        
        if primary_image:
            url = reverse('admin:products_productimage_change', args=[primary_image.id])
            return format_html(
                '<a href="{}" style="background: #2196F3; color: white; padding: 5px 12px; border-radius: 4px; text-decoration: none; font-size: 12px; display: inline-block;" title="Rasmni almashtirish">📷 Almashtirish</a>',
                url
            )
        else:
            url = reverse('admin:products_productimage_add') + f'?product={obj.id}'
            return format_html(
                '<a href="{}" style="background: #4CAF50; color: white; padding: 5px 12px; border-radius: 4px; text-decoration: none; font-size: 12px; display: inline-block;" title="Rasm qo\'shish">➕ Qo\'shish</a>',
                url
            )
    change_image_link.short_description = _('Rasmni tahrirlash')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description', 'short_description', 'category'),
            'description': 'Mahsulot haqida asosiy ma\'lumotlar. Name - mahsulot nomi, Slug - URL uchun ishlatiladi.'
        }),
        (_('Pricing'), {
            'fields': ('price', 'discount_percentage'),
            'description': 'Narxlash ma\'lumotlari. Price - asosiy narx (UZS), Discount - chegirma foizi.'
        }),
        (_('Inventory'), {
            'fields': ('sku', 'stock', 'brand', 'weight'),
            'description': 'Ombor va mahsulot xususiyatlari. SKU - mahsulot identifikatori (noyob bo\'lishi kerak), Stock - omborda qolgan miqdor.'
        }),
        (_('SEO'), {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
            'description': 'Qidiruv tizimlari uchun optimallashtirish.'
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_featured'),
            'description': 'Mahsulot holati. Active - saytda ko\'rinadi, Featured - asosiy sahifada ko\'rsatiladi.'
        }),
        (_('Statistics'), {
            'fields': ('views_count', 'sales_count'),
            'classes': ('collapse',),
            'description': 'Mahsulot statistikasi (faqat ko\'rish uchun).'
        }),
    )
    
    inlines = [ProductImageInline, ProductVariantInline]
    
    readonly_fields = ['views_count', 'sales_count']
    
    ordering = ['-created_at']
    
    actions = [
        'activate_products', 
        'deactivate_products',
        'make_featured',
        'remove_featured',
        'duplicate_products'
    ]
    
    def price_display(self, obj):
        """Display formatted price."""
        return f"{obj.price:,.0f} so'm"
    price_display.short_description = _('Price')
    price_display.admin_order_field = 'price'
    
    def discounted_price_display(self, obj):
        """Display discounted price if discount exists."""
        if obj.discount_percentage > 0:
            discounted = f"{obj.discounted_price:,.0f}"
            discount_pct = f"{obj.discount_percentage}"
            return format_html(
                '<span style="color: green; font-weight: bold;">{} so\'m</span> <br><small>(-{}%)</small>',
                discounted,
                discount_pct
            )
        return '-'
    discounted_price_display.short_description = _('Discounted Price')
    
    def stock_status(self, obj):
        """Display stock status with color coding."""
        if obj.stock == 0:
            return format_html('<span style="color: red; font-weight: bold;">Yo\'q</span>')
        elif obj.stock < 10:
            return format_html('<span style="color: orange;">{} dona</span>', obj.stock)
        else:
            return format_html('<span style="color: green;">{} dona</span>', obj.stock)
    stock_status.short_description = _('Stock')
    stock_status.admin_order_field = 'stock'
    
    def activate_products(self, request, queryset):
        """Activate selected products."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} ta mahsulot faollashtirildi.')
    activate_products.short_description = _('Activate selected products')
    
    def deactivate_products(self, request, queryset):
        """Deactivate selected products."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} ta mahsulot o\'chirildi.')
    deactivate_products.short_description = _('Deactivate selected products')
    
    def make_featured(self, request, queryset):
        """Mark products as featured."""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} ta mahsulot tanlangan mahsulotlar ro\'yxatiga qo\'shildi.')
    make_featured.short_description = _('Mark as featured')
    
    def remove_featured(self, request, queryset):
        """Remove products from featured."""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} ta mahsulot tanlangan mahsulotlardan olib tashlandi.')
    remove_featured.short_description = _('Remove from featured')
    
    def duplicate_products(self, request, queryset):
        """Duplicate selected products."""
        duplicated = 0
        for product in queryset:
            product.pk = None
            product.name = f"{product.name} (nusxa)"
            product.slug = f"{product.slug}-copy-{duplicated}"
            product.sku = f"{product.sku}-COPY-{duplicated}"
            product.save()
            duplicated += 1
        self.message_user(request, f'{duplicated} ta mahsulot nusxalandi.')
    duplicate_products.short_description = _('Duplicate selected products')
    
    def has_delete_permission(self, request, obj=None):
        """Allow admins to delete products."""
        return request.user.is_superuser or request.user.is_staff
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('category')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin interface for product images with upload/replace functionality."""
    list_display = ['product_link', 'image_preview_clickable', 'alt_text', 'is_primary', 'order', 'image_size', 'created_at']
    list_filter = ['is_primary', 'created_at', 'product__category']
    search_fields = ['product__name', 'alt_text']
    list_editable = ['is_primary', 'order']
    
    fields = ['product', 'image', 'image_preview_large', 'alt_text', 'is_primary', 'order']
    readonly_fields = ['image_preview_large', 'image_size']
    
    actions = ['make_primary', 'delete_images']
    
    def product_link(self, obj):
        """Display clickable product name."""
        url = reverse('admin:products_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = _('Mahsulot')
    
    def image_preview_clickable(self, obj):
        """Display clickable image thumbnail in list."""
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height: 60px; max-width: 60px; object-fit: cover; border-radius: 5px; border: 2px solid #4CAF50; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform=\'scale(1.5)\'" onmouseout="this.style.transform=\'scale(1)\'" /></a>', 
                obj.image.url,
                obj.image.url
            )
        return format_html('<span style="color: #999;">Rasm yo\'q</span>')
    image_preview_clickable.short_description = _('Rasm')
    
    def image_size(self, obj):
        """Display image file size."""
        if obj.image:
            try:
                size_bytes = obj.image.size
                if size_bytes < 1024:
                    return f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    return f"{size_bytes / 1024:.1f} KB"
                else:
                    return f"{size_bytes / (1024 * 1024):.1f} MB"
            except (FileNotFoundError, OSError):
                return format_html('<span style="color: #F44336;">Fayl yo\'q</span>')
        return "-"
    image_size.short_description = _('Fayl hajmi')
    
    def image_preview_large(self, obj):
        """Display large image preview in edit form with replacement instructions."""
        if obj.image:
            try:
                if not obj.image.storage.exists(obj.image.name):
                    return format_html(
                        '''<div style="padding: 20px; background: #FFEBEE; border-radius: 10px; border: 2px solid #F44336;">
                            <div style="font-size: 48px; margin-bottom: 10px; text-align: center;">⚠️</div>
                            <strong style="color: #D32F2F; font-size: 16px; display: block; text-align: center;">Fayl topilmadi!</strong><br>
                            <span style="color: #666; font-size: 13px; display: block; text-align: center;">
                            Database yozuvi mavjud, lekin fayl yo'q: <code>{}</code><br>
                            Iltimos, yangi rasm yuklang.
                            </span>
                        </div>''',
                        obj.image.name
                    )
                
                file_size = self.image_size(obj) if hasattr(self, 'image_size') else '-'
                created = obj.created_at.strftime('%d.%m.%Y %H:%M') if hasattr(obj, 'created_at') else '-'
                
                return format_html(
                    '''<div style="margin: 15px 0; padding: 15px; background: #f9f9f9; border-radius: 10px; border: 2px solid #ddd;">
                        <div style="margin-bottom: 10px;">
                            <strong style="color: #2196F3; font-size: 14px;">Joriy rasm:</strong>
                        </div>
                        <img src="{}" style="max-height: 400px; max-width: 600px; object-fit: contain; border: 2px solid #ddd; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />
                        <div style="margin-top: 15px; padding: 10px; background: #E3F2FD; border-radius: 5px; border-left: 4px solid #2196F3;">
                            <strong style="color: #1976D2;">📝 Rasmni almashtirish:</strong><br>
                            <span style="color: #666; font-size: 13px;">
                            1. Yuqoridagi "Image" maydonida "Choose File" tugmasini bosing<br>
                            2. Yangi rasmni tanlang<br>
                            3. "Save" tugmasini bosing<br>
                            4. Eski rasm avtomatik o'chiriladi va yangi rasm saqlanadi
                            </span>
                        </div>
                        <div style="margin-top: 10px; color: #666; font-size: 12px;">
                            📊 Fayl hajmi: <strong>{}</strong> | 
                            📅 Yuklangan: <strong>{}</strong>
                        </div>
                    </div>''',
                    obj.image.url,
                    file_size,
                    created
                )
            except Exception as e:
                return format_html(
                    '''<div style="padding: 20px; background: #FFF3E0; border-radius: 10px; border: 2px solid #FF9800;">
                        <strong style="color: #F57C00;">⚠️ Xatolik:</strong><br>
                        <span style="color: #666; font-size: 13px;">{}</span><br>
                        <span style="color: #666; font-size: 13px;">Iltimos, yangi rasm yuklang.</span>
                    </div>''',
                    str(e)
                )
        return format_html(
            '''<div style="padding: 20px; background: #FFF3E0; border-radius: 10px; border: 2px dashed #FF9800; text-align: center;">
                <div style="font-size: 48px; margin-bottom: 10px;">📷</div>
                <strong style="color: #F57C00; font-size: 16px;">Hozircha rasm yuklanmagan</strong><br>
                <span style="color: #666; font-size: 13px;">Yuqoridagi "Image" maydonidan rasm yuklang</span>
            </div>'''
        )
    image_preview_large.short_description = _('Rasm ko\'rinishi')
    
    def make_primary(self, request, queryset):
        """Make selected images primary for their products."""
        updated = 0
        for image in queryset:
            ProductImage.objects.filter(product=image.product).update(is_primary=False)
            image.is_primary = True
            image.save()
            updated += 1
        
        self.message_user(request, f'{updated} ta rasm asosiy qilib belgilandi.')
    make_primary.short_description = _('Tanlangan rasmlarni asosiy qilish')
    
    def delete_images(self, request, queryset):
        """Delete selected images."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} ta rasm o\'chirildi.')
    delete_images.short_description = _('Tanlangan rasmlarni o\'chirish')
    
    def has_delete_permission(self, request, obj=None):
        """Allow admins to delete product images."""
        return request.user.is_superuser or request.user.is_staff


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """Admin interface for product variants."""
    list_display = ['product', 'name', 'value', 'price_adjustment', 'stock', 'is_active']
    list_filter = ['is_active', 'name']
    search_fields = ['product__name', 'value']
    list_editable = ['stock', 'is_active']
    
    def has_delete_permission(self, request, obj=None):
        """Allow admins to delete product variants."""
        return request.user.is_superuser or request.user.is_staff