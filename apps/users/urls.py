"""
URL configuration for users app.
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile_view, name='profile'),

    path('addresses/add/', views.add_address_view, name='add_address'),
    path('addresses/<int:address_id>/edit/', views.edit_address_view, name='edit_address'),
    path('addresses/<int:address_id>/delete/', views.delete_address_view, name='delete_address'),

]