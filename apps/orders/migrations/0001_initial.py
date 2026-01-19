
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(editable=False, max_length=50, unique=True, verbose_name='order number')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('packed', 'Packed'), ('on_the_way', 'On the way'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=20, verbose_name='status')),
                ('customer_name', models.CharField(max_length=200, verbose_name='customer name')),
                ('customer_email', models.EmailField(max_length=254, verbose_name='customer email')),
                ('customer_phone', models.CharField(max_length=20, verbose_name='customer phone')),
                ('delivery_address', models.TextField(verbose_name='delivery address')),
                ('delivery_city', models.CharField(max_length=100, verbose_name='city')),
                ('delivery_region', models.CharField(blank=True, max_length=100, verbose_name='region')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='longitude')),
                ('currency', models.CharField(default='UZS', max_length=3, verbose_name='currency')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='subtotal')),
                ('delivery_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='delivery fee')),
                ('tax_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='tax amount')),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='discount amount')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='total amount')),
                ('payment_method', models.CharField(choices=[('cash', 'Cash on Delivery'), ('card', 'Plastic Card'), ('click', 'Click'), ('payme', 'Payme'), ('uzum', 'Uzum Bank')], max_length=50, verbose_name='payment method')),
                ('is_paid', models.BooleanField(default=False, verbose_name='paid')),
                ('paid_at', models.DateTimeField(blank=True, null=True, verbose_name='paid at')),
                ('customer_notes', models.TextField(blank=True, verbose_name='customer notes')),
                ('admin_notes', models.TextField(blank=True, verbose_name='admin notes')),
                ('cancellation_reason', models.TextField(blank=True, verbose_name='cancellation reason')),
                ('cancelled_at', models.DateTimeField(blank=True, null=True, verbose_name='cancelled at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('delivered_at', models.DateTimeField(blank=True, null=True, verbose_name='delivered at')),
                ('cancelled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cancelled_orders', to=settings.AUTH_USER_MODEL, verbose_name='cancelled by')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'orders',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255, verbose_name='product name')),
                ('product_sku', models.CharField(max_length=100, verbose_name='SKU')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='unit price')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='quantity')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='subtotal')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product', verbose_name='product')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.productvariant', verbose_name='variant')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
                'db_table': 'order_items',
            },
        ),
        migrations.CreateModel(
            name='OrderStatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_status', models.CharField(blank=True, max_length=20, verbose_name='from status')),
                ('to_status', models.CharField(max_length=20, verbose_name='to status')),
                ('notes', models.TextField(blank=True, verbose_name='notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='changed by')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_history', to='orders.order', verbose_name='order')),
            ],
            options={
                'verbose_name': 'Order Status History',
                'verbose_name_plural': 'Order Status Histories',
                'db_table': 'order_status_history',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['order_number'], name='orders_order_n_1336be_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['user', '-created_at'], name='orders_user_id_535113_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['status'], name='orders_status_762191_idx'),
        ),
    ]
