from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'gateway', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('gateway', 'status', 'created_at')
    readonly_fields = ('payload',)
