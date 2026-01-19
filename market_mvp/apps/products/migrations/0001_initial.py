
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=210, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=270, unique=True)),
                ('sku', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('currency', models.CharField(default='UZS', max_length=3)),
                ('is_active', models.BooleanField(default=True)),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.category')),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/%Y/%m/%d/')),
                ('alt', models.CharField(blank=True, max_length=255)),
                ('is_main', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
            options={
                'db_table': 'product_images',
            },
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sku', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('stock', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='products.product')),
            ],
            options={
                'db_table': 'product_variants',
            },
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['slug'], name='products_slug_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['sku'], name='products_sku_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['-created_at'], name='products_created_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='productvariant',
            unique_together={('product', 'sku')},
        ),
    ]
