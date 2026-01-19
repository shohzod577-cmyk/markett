"""
URL configuration for reviews app.
"""
from django.urls import path
from . import views
from .rate_view import rate_product_view

app_name = 'reviews'

urlpatterns = [
    path('create/<int:product_id>/', views.create_review_view, name='create'),
    path('vote/<int:review_id>/', views.vote_review_view, name='vote'),
    path('rate/<int:product_id>/', rate_product_view, name='rate'),
]