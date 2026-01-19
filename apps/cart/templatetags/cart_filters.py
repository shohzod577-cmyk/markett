"""
Custom template filters for cart app.
"""
from django import template
from core.services.currency import CurrencyService

register = template.Library()


@register.filter(name='format_price')
def format_price(amount, currency='UZS'):
    """
    Convert and format price with currency symbol.
    Amount is assumed to be in UZS (base currency).
    Usage: {{ price|format_price:currency }}
    """
    currency_service = CurrencyService()
    
    if currency != 'UZS':
        amount = currency_service.convert(amount, 'UZS', currency)
    
    return currency_service.format_price(amount, currency)


@register.filter(name='convert_currency')
def convert_currency(amount, currency='UZS'):
    """
    Convert amount to specified currency.
    Usage: {{ price|convert_currency:currency }}
    """
    currency_service = CurrencyService()
    return currency_service.convert(amount, 'UZS', currency)
