from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('stats/', views.stats, name='stats'),
    path('orders/<int:pk>/<str:action>/', views.order_action, name='order_action'),
]
