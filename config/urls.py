"""
Main URL Configuration for Market project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . views import home_view  # Add this import

urlpatterns = [
    # Django Admin (for emergency access only)
    path('django-admin-secret/', admin.site.urls),

    # Home
    path('', home_view, name='home'),  # Update this line

    # App URLs
    path('users/', include('apps.users.urls')),
    path('products/', include('apps.products.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
    path('payments/', include('apps.payments.urls')),
    path('reviews/', include('apps.reviews.urls')),

    # Custom Admin Dashboard
    path('dashboard/', include('apps.dashboard.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings. STATIC_URL, document_root=settings.STATIC_ROOT)