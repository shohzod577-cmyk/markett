
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
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'db_table': 'carts',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='quantity')),
                ('price_snapshot', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='price snapshot')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='cart.cart', verbose_name='cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='product')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productvariant', verbose_name='variant')),
            ],
            options={
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
                'db_table': 'cart_items',
                'unique_together': {('cart', 'product', 'variant')},
            },
        ),
    ]
