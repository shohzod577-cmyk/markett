
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='products.product', verbose_name='product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_products', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Product Like',
                'verbose_name_plural': 'Product Likes',
                'db_table': 'product_likes',
                'ordering': ['-created_at'],
                'unique_together': {('product', 'user')},
            },
        ),
    ]
