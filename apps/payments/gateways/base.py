"""
Base payment gateway interface for Market platform.
Abstract base class for all payment gateway implementations.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional
from decimal import Decimal


class PaymentGatewayError(Exception):
    """Custom exception for payment gateway errors."""
    pass


class BasePaymentGateway(ABC):
    """
    Abstract base class for payment gateway implementations.
    All payment gateways must inherit from this class.
    """

    def __init__(self):
        self.gateway_name = self.__class__.__name__

    @abstractmethod
    def create_payment(
            self,
            amount: Decimal,
            currency: str,
            order_id: str,
            description: str,
            **kwargs
    ) -> Dict:
        """
        Create a payment transaction.

        Args:
            amount: Payment amount
            currency: Currency code (UZS, USD, EUR)
            order_id: Order identifier
            description: Payment description
            **kwargs: Gateway-specific parameters

        Returns:
            Dict containing:
                - transaction_id: Gateway transaction ID
                - payment_url: URL for customer to complete payment
                - status:  Payment status
        """
        pass

    @abstractmethod
    def verify_payment(
            self,
            transaction_id: str,
            **kwargs
    ) -> Dict:
        """
        Verify payment status.

        Args:
            transaction_id: Gateway transaction ID
            **kwargs: Gateway-specific parameters

        Returns:
            Dict containing:
                - is_successful: Boolean
                - status: Payment status
                - amount:  Paid amount
                - details: Additional details
        """
        pass

    @abstractmethod
    def handle_webhook(
            self,
            payload: Dict,
            headers: Dict
    ) -> Dict:
        """
        Handle webhook callback from payment gateway.

        Args:
            payload: Webhook payload data
            headers: HTTP headers

        Returns:
            Dict containing processed webhook data
        """
        pass

    @abstractmethod
    def refund_payment(
            self,
            transaction_id: str,
            amount: Optional[Decimal] = None,
            reason: str = ''
    ) -> Dict:
        """
        Refund a payment.

        Args:
            transaction_id: Gateway transaction ID
            amount: Amount to refund (None = full refund)
            reason: Refund reason

        Returns:
            Dict containing refund status and details
        """
        pass

    def validate_signature(
            self,
            data: Dict,
            signature: str
    ) -> bool:
        """
        Validate webhook signature for security.

        Args:
            data: Webhook data
            signature: Signature to validate

        Returns:
            True if signature is valid
        """
        raise NotImplementedError("Signature validation not implemented")

    def log_transaction(
            self,
            transaction_type: str,
            data: Dict,
            success: bool = True
    ):
        """
        Log transaction for audit trail.

        Args:
            transaction_type: Type of transaction
            data: Transaction data
            success: Transaction success status
        """
        import logging
        logger = logging.getLogger(self.gateway_name)

        log_message = f"{transaction_type}:  {data}"
        if success:
            logger.info(log_message)
        else:
            logger.error(log_message)