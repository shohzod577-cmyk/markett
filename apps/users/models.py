"""
User models for Market platform.
Extended Django User model with additional fields for e-commerce.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Designed for scalability and future enhancements.
    """

    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(_('verified'), default=False)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)

    # User preferences
    preferred_currency = models.CharField(
        _('preferred currency'),
        max_length=3,
        default='UZS',
        choices=[('UZS', 'UZS'), ('USD', 'USD'), ('EUR', 'EUR')]
    )

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    # Security
    is_blocked = models.BooleanField(_('blocked'), default=False)
    blocked_reason = models.TextField(_('blocked reason'), blank=True, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """Return user's full name or email if name is not set."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email


class Address(models.Model):
    """
    User address model with geolocation support.
    Supports multiple addresses per user.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name=_('user')
    )

    # Address details
    label = models.CharField(_('label'), max_length=50, help_text='e.g., Home, Office')
    full_address = models.TextField(_('full address'))
    city = models.CharField(_('city'), max_length=100)
    region = models.CharField(_('region/state'), max_length=100, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)

    # Geolocation
    latitude = models.DecimalField(
        _('latitude'),
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        _('longitude'),
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    # Contact
    phone = models.CharField(_('phone number'), max_length=20)

    # Metadata
    is_default = models.BooleanField(_('default address'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        db_table = 'addresses'
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.label}"

    def save(self, *args, **kwargs):
        """Ensure only one default address per user."""
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """
    Extended user profile for additional information.
    One-to-one relationship with User. 
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('user')
    )

    # Personal information
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    gender = models.CharField(
        _('gender'),
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True
    )

    # Statistics
    total_orders = models.PositiveIntegerField(_('total orders'), default=0)
    total_spent = models.DecimalField(
        _('total spent'),
        max_digits=15,
        decimal_places=2,
        default=0
    )

    # Notifications
    email_notifications = models.BooleanField(_('email notifications'), default=True)
    sms_notifications = models.BooleanField(_('SMS notifications'), default=False)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"Profile of {self.user.email}"