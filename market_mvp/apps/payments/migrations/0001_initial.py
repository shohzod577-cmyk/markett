
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.PositiveIntegerField(blank=True, null=True)),
                ('gateway', models.CharField(choices=[('click', 'Click'), ('payme', 'Payme'), ('uzum', 'Uzum')], max_length=32)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('currency', models.CharField(default='UZS', max_length=8)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending', max_length=32)),
                ('reference', models.CharField(blank=True, max_length=255)),
                ('payload', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
