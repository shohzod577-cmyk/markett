from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls', namespace='users')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
]
