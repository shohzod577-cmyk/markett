"""
URL configuration for products app. 
"""
from django.urls import path
from . import views
from . import likes

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='list'),
    path('categories/', views.category_list_view, name='categories'),
    path('like/<int:product_id>/', likes.toggle_like, name='toggle_like'),
    path('like-status/<int:product_id>/', likes.get_like_status, name='like_status'),
    path('<slug:slug>/', views.product_detail_view, name='detail'),
]