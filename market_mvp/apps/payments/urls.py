from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('webhook/click/', views.click_webhook, name='click_webhook'),
    path('webhook/payme/', views.payme_webhook, name='payme_webhook'),
    path('webhook/uzum/', views.uzum_webhook, name='uzum_webhook'),
    path('initiate/<int:order_id>/<str:gateway>/', views.initiate, name='initiate'),
    path('mock/<int:txn_id>/complete/', views.mock_complete, name='mock_complete'),
]
