from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    preferred_currency = models.CharField(max_length=3, default='UZS')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email
