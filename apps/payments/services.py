"""
Payment service layer.
Business logic for payment processing.
"""
from decimal import Decimal
from typing import Dict, Optional
from django.db import transaction
from django.conf import settings

from .models import Payment, Transaction
from .gateways.click import ClickPaymentGateway
from .gateways.payme import PaymePaymentGateway
from apps.orders.models import Order


class PaymentService:
    """
    Service for managing payment operations.
    Gateway-agnostic payment processing.
    """

    def __init__(self):
        self.gateways = {
            'click': ClickPaymentGateway(),
            'payme': PaymePaymentGateway(),
        }

    @transaction.atomic
    def create_payment(
            self,
            order: Order,
            user,
            gateway: str,
            ip_address: str = '',
            user_agent: str = ''
    ) -> Payment:
        """
        Create payment record for order.
        """
        payment = Payment.objects.create(
            order=order,
            user=user,
            gateway=gateway,
            amount=order.total_amount,
            currency=order.currency,
            ip_address=ip_address,
            user_agent=user_agent,
            status=Payment.STATUS_PENDING
        )

        Transaction.objects.create(
            payment=payment,
            transaction_type=Transaction.TYPE_AUTHORIZATION,
            status='pending',
            ip_address=ip_address
        )

        return payment

    def initiate_payment(self, payment: Payment) -> Dict:
        """
        Initiate payment with gateway.
        Returns payment URL for redirect.
        """
        gateway = self.gateways.get(payment.gateway)

        if not gateway:
            return {
                'success': False,
                'error': f'Unsupported payment gateway: {payment.gateway}'
            }

        try:
            return_url = f"{settings.SITE_URL}/payments/success/? payment_id={payment.payment_id}"

            result = gateway.create_payment(
                amount=payment.amount,
                currency=payment.currency,
                order_id=payment.order.order_number,
                description=f"Order #{payment.order.order_number}",
                return_url=return_url
            )

            payment.gateway_transaction_id = result['transaction_id']
            payment.status = Payment.STATUS_PROCESSING
            payment.gateway_response = result
            payment.save()

            Transaction.objects.create(
                payment=payment,
                transaction_type=Transaction.TYPE_AUTHORIZATION,
                status='processing',
                gateway_transaction_id=result['transaction_id'],
                request_data={'action': 'initiate'},
                response_data=result
            )

            return {
                'success': True,
                'payment_url': result['payment_url']
            }

        except Exception as e:
            payment.mark_as_failed(error_message=str(e))

            return {
                'success': False,
                'error': str(e)
            }

    def verify_payment(self, payment: Payment) -> Dict:
        """
        Verify payment status with gateway.
        """
        gateway = self.gateways.get(payment.gateway)

        if not gateway:
            return {
                'is_successful': False,
                'error': 'Unsupported payment gateway'
            }

        try:
            result = gateway.verify_payment(
                transaction_id=payment.gateway_transaction_id
            )

            Transaction.objects.create(
                payment=payment,
                transaction_type=Transaction.TYPE_CAPTURE,
                status='completed' if result['is_successful'] else 'failed',
                gateway_transaction_id=payment.gateway_transaction_id,
                response_data=result
            )

            if result['is_successful']:
                payment.mark_as_completed()

            return result

        except Exception as e:
            return {
                'is_successful': False,
                'error': str(e)
            }

    @transaction.atomic
    def refund_payment(
            self,
            payment: Payment,
            amount: Optional[Decimal] = None,
            reason: str = ''
    ) -> Dict:
        """
        Refund payment.
        """
        gateway = self.gateways.get(payment.gateway)

        if not gateway:
            return {
                'success': False,
                'error': 'Unsupported payment gateway'
            }

        try:
            result = gateway.refund_payment(
                transaction_id=payment.gateway_transaction_id,
                amount=amount,
                reason=reason
            )

            if result['success']:
                payment.status = Payment.STATUS_REFUNDED
                payment.save()

            Transaction.objects.create(
                payment=payment,
                transaction_type=Transaction.TYPE_REFUND,
                amount=amount or payment.amount,
                status='completed' if result['success'] else 'failed',
                gateway_transaction_id=payment.gateway_transaction_id,
                request_data={'reason': reason},
                response_data=result
            )

            return result

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }