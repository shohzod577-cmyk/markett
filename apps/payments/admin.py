from django.contrib import admin
from .models import Payment, Transaction


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'order', 'gateway', 'amount', 'status', 'created_at']
    list_filter = ['gateway', 'status']
    search_fields = ['payment_id', 'order__order_number', 'gateway_transaction_id']
    readonly_fields = ['payment_id', 'gateway_response', 'created_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['payment', 'transaction_type', 'amount', 'status', 'created_at']
    list_filter = ['transaction_type', 'status']
    readonly_fields = ['request_data', 'response_data', 'created_at']