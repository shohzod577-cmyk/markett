from django.contrib import admin

from .models import Order, OrderItem
from .models import OrderAction


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'variant', 'price', 'quantity')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]
    readonly_fields = ('total',)


class OrderActionInline(admin.TabularInline):
    model = OrderAction
    readonly_fields = ('action', 'performed_by', 'notes', 'created_at')
    extra = 0


@admin.register(OrderAction)
class OrderActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'action', 'performed_by', 'created_at')
    list_filter = ('action', 'created_at')
    readonly_fields = ('created_at',)
