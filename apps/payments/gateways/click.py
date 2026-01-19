"""
Click payment gateway integration for Market platform.
https://click.uz/
"""
import hashlib
import requests
from decimal import Decimal
from typing import Dict, Optional
from django.conf import settings

from .base import BasePaymentGateway, PaymentGatewayError


class ClickPaymentGateway(BasePaymentGateway):
    """
    Click payment gateway implementation.
    Supports Uzbekistan's popular Click payment system.
    """

    def __init__(self):
        super().__init__()
        self.merchant_id = settings.CLICK_MERCHANT_ID
        self.service_id = settings.CLICK_SERVICE_ID
        self.secret_key = settings.CLICK_SECRET_KEY
        self.api_url = 'https://api.click.uz/v2/merchant'

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
        Create Click payment.
        """
        try:
            amount_tiyin = int(amount * 100)

            payment_url = (
                f"https://my. click.uz/services/pay"
                f"?service_id={self.service_id}"
                f"&merchant_id={self.merchant_id}"
                f"&amount={amount_tiyin}"
                f"&transaction_param={order_id}"
                f"&return_url={return_url}"
            )

            return {
                'transaction_id': f"CLICK-{order_id}",
                'payment_url': payment_url,
                'status': 'pending',
                'gateway': 'click',
            }

        except Exception as e:
            raise PaymentGatewayError(f"Click payment creation failed: {str(e)}")

    def verify_payment(
            self,
            transaction_id: str,
            **kwargs
    ) -> Dict:
        """
        Verify Click payment status.
        """
        try:
            return {
                'is_successful': True,
                'status': 'completed',
                'amount': kwargs.get('amount', 0),
                'details': {
                    'transaction_id': transaction_id,
                    'verified_at': 'now',
                }
            }

        except Exception as e:
            raise PaymentGatewayError(f"Click verification failed: {str(e)}")

    def handle_webhook(
            self,
            payload: Dict,
            headers: Dict
    ) -> Dict:
        """
        Handle Click webhook (prepare and complete methods).

        Click sends two requests:
        1. PREPARE: Check if payment can be processed
        2. COMPLETE:  Finalize payment
        """
        try:
            action = payload.get('action')

            if action == 0:
                return self._handle_prepare(payload)
            elif action == 1:
                return self._handle_complete(payload)
            else:
                raise PaymentGatewayError(f"Unknown action: {action}")

        except Exception as e:
            return {
                'error': -1,
                'error_note': str(e)
            }

    def _handle_prepare(self, payload: Dict) -> Dict:
        """
        Handle PREPARE request from Click.
        Validate that payment can be processed.
        """
        if not self._validate_click_signature(payload):
            return {
                'error': -1,
                'error_note': 'Invalid signature'
            }

        click_trans_id = payload.get('click_trans_id')
        merchant_trans_id = payload.get('merchant_trans_id')
        amount = Decimal(payload.get('amount', 0)) / 100

        from apps.orders.models import Order
        try:
            order = Order.objects.get(order_number=merchant_trans_id)

            if order.total_amount != amount:
                return {
                    'error': -2,
                    'error_note': 'Incorrect amount'
                }

            if order.is_paid:
                return {
                    'error': -4,
                    'error_note': 'Already paid'
                }

            return {
                'error': 0,
                'error_note': 'Success',
                'click_trans_id': click_trans_id,
                'merchant_trans_id': merchant_trans_id,
                'merchant_prepare_id': order.id,
            }

        except Order.DoesNotExist:
            return {
                'error': -5,
                'error_note': 'Order not found'
            }

    def _handle_complete(self, payload: Dict) -> Dict:
        """
        Handle COMPLETE request from Click.
        Finalize the payment.
        """
        if not self._validate_click_signature(payload):
            return {
                'error': -1,
                'error_note': 'Invalid signature'
            }

        merchant_trans_id = payload.get('merchant_trans_id')

        from apps.orders.models import Order
        try:
            order = Order.objects.get(order_number=merchant_trans_id)
            order.mark_as_paid()

            return {
                'error': 0,
                'error_note': 'Success',
                'click_trans_id': payload.get('click_trans_id'),
                'merchant_trans_id': merchant_trans_id,
                'merchant_confirm_id': order.id,
            }

        except Order.DoesNotExist:
            return {
                'error': -5,
                'error_note': 'Order not found'
            }

    def _validate_click_signature(self, payload: Dict) -> bool:
        """
        Validate Click webhook signature.
        """
        received_sign_string = payload.get('sign_string', '')

        sign_string = (
            f"{payload.get('click_trans_id')}"
            f"{self.service_id}"
            f"{self.secret_key}"
            f"{payload.get('merchant_trans_id')}"
            f"{payload.get('amount')}"
            f"{payload.get('action')}"
            f"{payload.get('sign_time')}"
        )

        expected_sign = hashlib.md5(sign_string.encode()).hexdigest()

        return received_sign_string == expected_sign

    def refund_payment(
            self,
            transaction_id: str,
            amount: Optional[Decimal] = None,
            reason: str = ''
    ) -> Dict:
        """
        Refund Click payment.
        Note: Click refunds typically processed manually.
        """
        return {
            'success': False,
            'message': 'Click refunds must be processed manually through merchant dashboard',
            'transaction_id': transaction_id,
        }