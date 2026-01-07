"""
URL configuration for dashboard app.
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard home
    path('', views.dashboard_home_view, name='home'),

    # Users management
    path('users/', views.users_list_view, name='users_list'),
    path('users/<int:user_id>/', views.user_detail_view, name='user_detail'),
    path('users/<int:user_id>/block/', views.block_user_view, name='block_user'),

    # Products management
    path('products/', views.products_list_view, name='products_list'),

    # Orders management
    path('orders/', views.orders_list_view, name='orders_list'),
    path('orders/<int:order_id>/', views.order_detail_view, name='order_detail'),

    # Reviews moderation
    path('reviews/', views.reviews_list_view, name='reviews_list'),
    path('reviews/<int:review_id>/moderate/', views.review_moderate_view, name='review_moderate'),

    # Analytics API
    path('api/analytics/', views.analytics_api_view, name='analytics_api'),
]