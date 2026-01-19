from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_verified', 'created_at']
    list_filter = ['is_staff', 'is_verified', 'is_blocked']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'avatar', 'preferred_currency', 'is_verified', 'is_blocked', 'blocked_reason')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        """Allow superusers to delete users."""
        return request.user.is_superuser


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'label', 'city', 'is_default', 'created_at']
    list_filter = ['is_default', 'city']
    search_fields = ['user__email', 'full_address', 'city']
    
    def has_delete_permission(self, request, obj=None):
        """Allow admins to delete addresses."""
        return request.user.is_superuser or request.user.is_staff


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_orders', 'total_spent']
    search_fields = ['user__email']
    
    def has_delete_permission(self, request, obj=None):
        """Allow superusers to delete user profiles."""
        return request.user.is_superuser