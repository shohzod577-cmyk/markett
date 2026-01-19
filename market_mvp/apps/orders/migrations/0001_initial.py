
import django.db.models.deletion
import django.utils.timezone
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
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(blank=True, max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('address_line1', models.CharField(max_length=255)),
                ('address_line2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=120)),
                ('postal_code', models.CharField(blank=True, max_length=30)),
                ('country', models.CharField(default='Uzbekistan', max_length=80)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=32)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.productvariant')),
            ],
        ),
    ]
