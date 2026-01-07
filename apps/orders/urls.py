"""
URL configuration for orders app.
"""
from django. urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('', views.order_list_view, name='list'),
    path('<int:order_id>/', views.order_detail_view, name='detail'),
    path('<int:order_id>/cancel/', views.cancel_order_view, name='cancel'),
    path('<int:order_id>/invoice/', views.download_invoice_view, name='invoice'),
]