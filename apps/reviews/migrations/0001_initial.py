
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(help_text='1-5 stars', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='rating')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('comment', models.TextField(verbose_name='comment')),
                ('is_verified_purchase', models.BooleanField(default=False, help_text='User purchased this product', verbose_name='verified purchase')),
                ('is_approved', models.BooleanField(default=False, verbose_name='approved')),
                ('is_flagged', models.BooleanField(default=False, verbose_name='flagged')),
                ('moderation_notes', models.TextField(blank=True, verbose_name='moderation notes')),
                ('helpful_count', models.PositiveIntegerField(default=0, verbose_name='helpful count')),
                ('not_helpful_count', models.PositiveIntegerField(default=0, verbose_name='not helpful count')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('order', models.ForeignKey(blank=True, help_text='Order that verifies this purchase', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='orders.order', verbose_name='order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='products.product', verbose_name='product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'db_table': 'reviews',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='reviews/', verbose_name='image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='reviews.review', verbose_name='review')),
            ],
            options={
                'verbose_name': 'Review Image',
                'verbose_name_plural': 'Review Images',
                'db_table': 'review_images',
            },
        ),
        migrations.CreateModel(
            name='ReviewVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(choices=[('helpful', 'Helpful'), ('not_helpful', 'Not Helpful')], max_length=20, verbose_name='vote type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='reviews.review', verbose_name='review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_votes', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Review Vote',
                'verbose_name_plural': 'Review Votes',
                'db_table': 'review_votes',
            },
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['product', '-created_at'], name='reviews_product_500bf4_idx'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['is_approved'], name='reviews_is_appr_807bf4_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('product', 'user', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='reviewvote',
            unique_together={('review', 'user')},
        ),
    ]
