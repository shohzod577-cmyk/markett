"""
Review and rating models for Market e-commerce platform.
Verified buyer reviews with fraud prevention.
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.products.models import Product
from apps.orders.models import Order


class Review(models.Model):
    """
    Product review model with verification system.
    Only verified buyers can leave reviews.
    """

    # Relationships
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('product')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('user')
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='reviews',
        verbose_name=_('order'),
        help_text='Order that verifies this purchase'
    )

    # Rating
    rating = models.PositiveSmallIntegerField(
        _('rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='1-5 stars'
    )

    # Review content
    title = models.CharField(_('title'), max_length=200)
    comment = models.TextField(_('comment'))

    # Verification
    is_verified_purchase = models.BooleanField(
        _('verified purchase'),
        default=False,
        help_text='User purchased this product'
    )

    # Moderation
    is_approved = models.BooleanField(_('approved'), default=False)
    is_flagged = models.BooleanField(_('flagged'), default=False)
    moderation_notes = models.TextField(_('moderation notes'), blank=True)

    # Helpful votes
    helpful_count = models.PositiveIntegerField(_('helpful count'), default=0)
    not_helpful_count = models.PositiveIntegerField(_('not helpful count'), default=0)

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        db_table = 'reviews'
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at']
        unique_together = ['product', 'user', 'order']
        indexes = [
            models.Index(fields=['product', '-created_at']),
            models.Index(fields=['is_approved']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.rating}★)"

    @property
    def helpful_percentage(self):
        """Calculate percentage of helpful votes."""
        total_votes = self.helpful_count + self.not_helpful_count
        if total_votes == 0:
            return 0
        return round((self.helpful_count / total_votes) * 100)


class ReviewImage(models.Model):
    """
    Images attached to product reviews.
    Customers can upload photos with their reviews.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('review')
    )

    image = models.ImageField(_('image'), upload_to='reviews/')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        db_table = 'review_images'
        verbose_name = _('Review Image')
        verbose_name_plural = _('Review Images')

    def __str__(self):
        return f"Image for review #{self.review.id}"


class ReviewVote(models.Model):
    """
    Track user votes on review helpfulness.
    Prevents duplicate voting. 
    """

    VOTE_HELPFUL = 'helpful'
    VOTE_NOT_HELPFUL = 'not_helpful'

    VOTE_CHOICES = [
        (VOTE_HELPFUL, _('Helpful')),
        (VOTE_NOT_HELPFUL, _('Not Helpful')),
    ]

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name=_('review')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='review_votes',
        verbose_name=_('user')
    )

    vote_type = models.CharField(
        _('vote type'),
        max_length=20,
        choices=VOTE_CHOICES
    )

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        db_table = 'review_votes'
        verbose_name = _('Review Vote')
        verbose_name_plural = _('Review Votes')
        unique_together = ['review', 'user']

    def __str__(self):
        return f"{self.user.email} - {self.vote_type}"