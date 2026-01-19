"""
Custom middleware for Market platform.
"""
from django.conf import settings


class CurrencyMiddleware:
    """
    Middleware to handle currency selection across the site.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'currency' not in request.session:
            if request.user.is_authenticated and hasattr(request.user, 'preferred_currency'):
                request.session['currency'] = request.user. preferred_currency
            else:
                request.session['currency'] = settings.DEFAULT_CURRENCY

        if 'currency' in request.GET:
            new_currency = request.GET['currency']
            if new_currency in settings.SUPPORTED_CURRENCIES:
                request. session['currency'] = new_currency

                if request.user.is_authenticated:
                    request. user.preferred_currency = new_currency
                    request.user. save(update_fields=['preferred_currency'])

        response = self. get_response(request)
        return response