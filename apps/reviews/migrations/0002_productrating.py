
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_productlike'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(help_text='1-5 stars', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='rating')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_ratings', to='products.product', verbose_name='product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_ratings', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Product Rating',
                'verbose_name_plural': 'Product Ratings',
                'db_table': 'product_ratings',
                'unique_together': {('product', 'user')},
            },
        ),
    ]
