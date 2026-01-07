from django.contrib import admin
from .models import Review, ReviewImage, ReviewVote


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_verified_purchase', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'is_verified_purchase', 'rating']
    search_fields = ['product__name', 'user__email', 'title']
    actions = ['approve_reviews', 'flag_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True, is_flagged=False)

    approve_reviews.short_description = "Approve selected reviews"

    def flag_reviews(self, request, queryset):
        queryset.update(is_flagged=True)

    flag_reviews.short_description = "Flag selected reviews"