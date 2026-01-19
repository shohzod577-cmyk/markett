"""
Main URL Configuration for Market project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from . views import (
    home_view, custom_404_view, custom_500_view, custom_403_view, custom_400_view,
    about_view, contact_view, faq_view, help_center_view, shipping_info_view,
    returns_view, track_order_view, careers_view, press_view, blog_view, blog_detail_view,
    set_language_view
)

handler404 = custom_404_view
handler500 = custom_500_view
handler403 = custom_403_view
handler400 = custom_400_view

urlpatterns = [
    path('i18n/setlang/', set_language_view, name='set_language'),
    
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'images/halol-savdo-baraka-circle.svg', permanent=True)),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),

    path('users/', include('apps.users.urls')),
    path('products/', include('apps.products.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
    path('payments/', include('apps.payments.urls')),
    path('reviews/', include('apps.reviews.urls')),

    path('dashboard/', include('apps.dashboard.urls')),
    
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('faq/', faq_view, name='faq'),
    path('help/', help_center_view, name='help_center'),
    path('shipping/', shipping_info_view, name='shipping_info'),
    path('returns/', returns_view, name='returns'),
    path('track/', track_order_view, name='track_order'),
    path('careers/', careers_view, name='careers'),
    path('press/', press_view, name='press'),
    path('blog/', blog_view, name='blog'),
    path('blog/<slug:slug>/', blog_detail_view, name='blog_detail'),
    
    path('test-404/', lambda r: custom_404_view(r, None), name='test_404'),
    path('test-500/', lambda r: custom_500_view(r), name='test_500'),
    path('test-403/', lambda r: custom_403_view(r, None), name='test_403'),
    path('test-400/', lambda r: custom_400_view(r, None), name='test_400'),
    
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings. STATIC_URL, document_root=settings.STATIC_ROOT)