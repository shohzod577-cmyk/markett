"""
URL configuration for payments app.
"""
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment processing
    path('process/<int:order_id>/', views.payment_process_view, name='process'),
    path('success/', views.payment_success_view, name='success'),
    path('cancel/', views.payment_cancel_view, name='cancel'),

    # Webhooks (no login required)
    path('webhook/click/', views.click_webhook_view, name='webhook_click'),
    path('webhook/payme/', views.payme_webhook_view, name='webhook_payme'),
]