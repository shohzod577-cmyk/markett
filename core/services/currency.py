"""
Currency conversion service for Market platform.
Centralized currency management with real-time rates.
"""
import requests
from decimal import Decimal
from django.core.cache import cache
from django.conf import settings
from typing import Dict, Optional


class CurrencyService:
    """
    Service for currency conversion and rate management.
    Uses external API with caching for performance.
    """

    # Cache settings
    CACHE_KEY = 'currency_rates'
    CACHE_TIMEOUT = 3600  # 1 hour

    # API endpoints
    API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'
    FALLBACK_RATES = {
        'UZS': Decimal('12450.00'),  # 1 USD = 12,450 UZS (example)
        'USD': Decimal('1.00'),
        'EUR': Decimal('0.92'),
    }

    def __init__(self):
        self.base_currency = settings.BASE_CURRENCY
        self.supported_currencies = settings.SUPPORTED_CURRENCIES

    def get_rates(self) -> Dict[str, Decimal]:
        """
        Get current exchange rates.
        Uses cache to minimize API calls.
        """
        # Try to get from cache
        rates = cache.get(self.CACHE_KEY)

        if rates is None:
            # Fetch from API
            rates = self._fetch_rates_from_api()

            if rates:
                # Cache the rates
                cache.set(self.CACHE_KEY, rates, self.CACHE_TIMEOUT)
            else:
                # Use fallback rates if API fails
                rates = self.FALLBACK_RATES

        return rates

    def _fetch_rates_from_api(self) -> Optional[Dict[str, Decimal]]:
        """
        Fetch exchange rates from external API.
        """
        try:
            response = requests.get(self.API_URL, timeout=5)
            response.raise_for_status()
            data = response.json()

            # Convert to Decimal for precision
            rates = {
                currency: Decimal(str(rate))
                for currency, rate in data['rates'].items()
                if currency in self.supported_currencies
            }

            return rates

        except Exception as e:
            print(f"Error fetching currency rates: {e}")
            return None

    def convert(
            self,
            amount: Decimal,
            from_currency: str,
            to_currency: str
    ) -> Decimal:
        """
        Convert amount from one currency to another.

        Args:
            amount: Amount to convert
            from_currency:  Source currency code (e.g., 'UZS')
            to_currency:  Target currency code (e.g., 'USD')

        Returns:
            Converted amount as Decimal
        """
        if from_currency == to_currency:
            return amount

        rates = self.get_rates()

        # Convert to USD first (base currency)
        if from_currency != 'USD':
            amount = amount / rates.get(from_currency, Decimal('1'))

        # Convert from USD to target currency
        if to_currency != 'USD':
            amount = amount * rates.get(to_currency, Decimal('1'))

        return amount.quantize(Decimal('0.01'))

    def format_price(
            self,
            amount: Decimal,
            currency: str
    ) -> str:
        """
        Format price with currency symbol.

        Args:
            amount: Price amount
            currency:  Currency code

        Returns:
            Formatted price string
        """
        symbols = {
            'UZS': 'so\'m',
            'USD': '$',
            'EUR': '€',
        }

        symbol = symbols.get(currency, currency)

        if currency == 'UZS':
            # Format UZS without decimals
            return f"{int(amount):,} {symbol}".replace(',', ' ')
        else:
            # Format with decimals
            return f"{symbol}{amount: ,.2f}"

    def get_display_price(
            self,
            base_price: Decimal,
            target_currency: str
    ) -> Dict[str, any]:
        """
        Get price converted and formatted for display.

        Args:
            base_price:  Price in base currency (UZS)
            target_currency: Target currency for display

        Returns:
            Dict with raw and formatted price
        """
        converted = self.convert(base_price, self.base_currency, target_currency)

        return {
            'amount': converted,
            'currency': target_currency,
            'formatted': self.format_price(converted, target_currency),
        }


def currency_context(request):
    """
    Context processor for currency in templates.
    """
    currency = request.session.get('currency', settings.DEFAULT_CURRENCY)

    return {
        'current_currency': currency,
        'supported_currencies': settings.SUPPORTED_CURRENCIES,
        'currency_service': CurrencyService(),
    }