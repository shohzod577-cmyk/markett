"""
Payme payment gateway integration for Market platform.
https://payme.uz/
"""
import base64
import hashlib
import requests
from decimal import Decimal
from typing import Dict, Optional
from django.conf import settings

from .base import BasePaymentGateway, PaymentGatewayError


class PaymePaymentGateway(BasePaymentGateway):
    """
    Payme payment gateway implementation.
    Uzbekistan's leading payment system.
    """

    def __init__(self):
        super().__init__()
        self.merchant_id = settings.PAYME_MERCHANT_ID
        self.secret_key = settings.PAYME_SECRET_KEY
        self.endpoint = settings.PAYME_ENDPOINT

    def create_payment(
            self,
            amount: Decimal,
            currency: str,
            order_id: str,
            description: str,
            return_url: str = '',
            **kwargs
    ) -> Dict:
        """
        Create Payme payment link.
        """
        try:
            amount_tiyin = int(amount * 100)

            order_data = f"m={self.merchant_id};ac. order_id={order_id};a={amount_tiyin}"
            encoded_data = base64.b64encode(order_data.encode()).decode()

            payment_url = f"https://checkout.paycom.uz/{encoded_data}"

            return {
                'transaction_id': f"PAYME-{order_id}",
                'payment_url': payment_url,
                'status': 'pending',
                'gateway': 'payme',
            }

        except Exception as e:
            raise PaymentGatewayError(f"Payme payment creation failed: {str(e)}")

    def verify_payment(
            self,
            transaction_id: str,
            **kwargs
    ) -> Dict:
        """
        Verify Payme payment status via JSON-RPC.
        """
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "CheckTransaction",
                "params": {
                    "id": transaction_id
                },
                "id": 1
            }

            headers = {
                'Content-Type': 'application/json',
                'X-Auth': self._generate_auth_header()
            }

            response = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=10
            )

            data = response.json()

            if 'result' in data:
                result = data['result']
                return {
                    'is_successful': result.get('state') == 2,
                    'status': self._map_payme_state(result.get('state')),
                    'amount': Decimal(result.get('amount', 0)) / 100,
                    'details': result
                }
            else:
                raise PaymentGatewayError(data.get('error', {}).get('message', 'Unknown error'))

        except Exception as e:
            raise PaymentGatewayError(f"Payme verification failed: {str(e)}")

    def handle_webhook(
            self,
            payload: Dict,
            headers: Dict
    ) -> Dict:
        """
        Handle Payme JSON-RPC webhook.

        Payme uses JSON-RPC 2.0 protocol with methods:
        - CheckPerformTransaction
        - CreateTransaction
        - PerformTransaction
        - CancelTransaction
        - CheckTransaction
        """
        try:
            if not self._validate_auth_header(headers.get('Authorization', '')):
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32504,
                        "message": "Insufficient privileges"
                    },
                    "id": payload.get('id')
                }

            method = payload.get('method')
            params = payload.get('params', {})

            if method == 'CheckPerformTransaction':
                return self._check_perform_transaction(params, payload.get('id'))
            elif method == 'CreateTransaction':
                return self._create_transaction(params, payload.get('id'))
            elif method == 'PerformTransaction':
                return self._perform_transaction(params, payload.get('id'))
            elif method == 'CancelTransaction':
                return self._cancel_transaction(params, payload.get('id'))
            elif method == 'CheckTransaction':
                return self._check_transaction(params, payload.get('id'))
            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": "Method not found"
                    },
                    "id": payload.get('id')
                }

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32400,
                    "message": str(e)
                },
                "id": payload.get('id')
            }

    def _check_perform_transaction(self, params: Dict, request_id: int) -> Dict:
        """Check if transaction can be performed."""
        from apps.orders.models import Order

        try:
            order_id = params['account']['order_id']
            amount = Decimal(params['amount']) / 100

            order = Order.objects.get(order_number=order_id)

            if order.total_amount != amount:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -31001,
                        "message": "Incorrect amount"
                    },
                    "id": request_id
                }

            if order.is_paid:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -31099,
                        "message": "Order already paid"
                    },
                    "id": request_id
                }

            return {
                "jsonrpc": "2.0",
                "result": {
                    "allow": True
                },
                "id": request_id
            }

        except Order.DoesNotExist:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -31050,
                    "message": "Order not found"
                },
                "id": request_id
            }

    def _create_transaction(self, params: Dict, request_id: int) -> Dict:
        """Create transaction in pending state."""
        from apps.payments.models import Payment
        from apps.orders.models import Order

        try:
            transaction_id = params['id']
            order_id = params['account']['order_id']
            amount = Decimal(params['amount']) / 100

            order = Order.objects.get(order_number=order_id)

            payment, created = Payment.objects.get_or_create(
                gateway_transaction_id=transaction_id,
                defaults={
                    'order': order,
                    'user': order.user,
                    'gateway': 'payme',
                    'amount': amount,
                    'currency': order.currency,
                    'status': 'processing'
                }
            )

            return {
                "jsonrpc": "2.0",
                "result": {
                    "create_time": int(payment.created_at.timestamp() * 1000),
                    "transaction": str(payment.id),
                    "state": 1
                },
                "id": request_id
            }

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -31008,
                    "message": str(e)
                },
                "id": request_id
            }

    def _perform_transaction(self, params: Dict, request_id: int) -> Dict:
        """Complete the transaction."""
        from apps.payments.models import Payment

        try:
            transaction_id = params['id']

            payment = Payment.objects.get(gateway_transaction_id=transaction_id)
            payment.mark_as_completed(transaction_id)

            return {
                "jsonrpc": "2.0",
                "result": {
                    "transaction": str(payment.id),
                    "perform_time": int(payment.completed_at.timestamp() * 1000),
                    "state": 2
                },
                "id": request_id
            }

        except Payment.DoesNotExist:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -31003,
                    "message": "Transaction not found"
                },
                "id": request_id
            }

    def _cancel_transaction(self, params: Dict, request_id: int) -> Dict:
        """Cancel transaction."""
        from apps.payments.models import Payment

        try:
            transaction_id = params['id']

            payment = Payment.objects.get(gateway_transaction_id=transaction_id)
            payment.status = 'cancelled'
            payment.save()

            return {
                "jsonrpc": "2.0",
                "result": {
                    "transaction": str(payment.id),
                    "cancel_time": int(payment.updated_at.timestamp() * 1000),
                    "state": -1
                },
                "id": request_id
            }

        except Payment.DoesNotExist:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -31003,
                    "message": "Transaction not found"
                },
                "id": request_id
            }

    def _check_transaction(self, params: Dict, request_id: int) -> Dict:
        """Check transaction status."""
        from apps.payments.models import Payment

        try:
            transaction_id = params['id']

            payment = Payment.objects.get(gateway_transaction_id=transaction_id)

            state_map = {
                'pending': 0,
                'processing': 1,
                'completed': 2,
                'cancelled': -1,
                'failed': -2,
            }

            return {
                "jsonrpc": "2.0",
                "result": {
                    "create_time": int(payment.created_at.timestamp() * 1000),
                    "perform_time": int(payment.completed_at.timestamp() * 1000) if payment.completed_at else 0,
                    "transaction": str(payment.id),
                    "state": state_map.get(payment.status, 0)
                },
                "id": request_id
            }

        except Payment.DoesNotExist:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -31003,
                    "message": "Transaction not found"
                },
                "id": request_id
            }

    def _generate_auth_header(self) -> str:
        """Generate authorization header for API requests."""
        credentials = f"{self.merchant_id}:{self.secret_key}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    def _validate_auth_header(self, auth_header: str) -> bool:
        """Validate authorization header from webhook."""
        expected = self._generate_auth_header()
        return auth_header == expected

    def _map_payme_state(self, state: int) -> str:
        """Map Payme state to our status."""
        mapping = {
            0: 'pending',
            1: 'processing',
            2: 'completed',
            -1: 'cancelled',
            -2: 'failed',
        }
        return mapping.get(state, 'pending')

    def refund_payment(
            self,
            transaction_id: str,
            amount: Optional[Decimal] = None,
            reason: str = ''
    ) -> Dict:
        """
        Refund Payme payment.
        """
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "CancelTransaction",
                "params": {
                    "id": transaction_id,
                    "reason": 3
                },
                "id": 1
            }

            headers = {
                'Content-Type': 'application/json',
                'X-Auth': self._generate_auth_header()
            }

            response = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=10
            )

            data = response.json()

            if 'result' in data:
                return {
                    'success': True,
                    'transaction_id': transaction_id,
                    'details': data['result']
                }
            else:
                return {
                    'success': False,
                    'error': data.get('error', {}).get('message')
                }

        except Exception as e:
            raise PaymentGatewayError(f"Payme refund failed: {str(e)}")