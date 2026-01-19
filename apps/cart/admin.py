from django. contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__email']
    inlines = [CartItemInline]
    
    def has_delete_permission(self, request, obj=None):
        """Allow admins to delete carts."""
        return request.user.is_superuser or request.user.is_staff