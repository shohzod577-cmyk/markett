"""
URL configuration for products app. 
"""
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='list'),
    path('categories/', views.category_list_view, name='categories'),
    path('<slug:slug>/', views.product_detail_view, name='detail'),
]