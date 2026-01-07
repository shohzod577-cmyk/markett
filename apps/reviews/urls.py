"""
URL configuration for reviews app.
"""
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:product_id>/', views.create_review_view, name='create'),
    path('vote/<int:review_id>/', views.vote_review_view, name='vote'),
]