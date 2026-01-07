"""
Email service for Market platform.
Handles transactional emails with templates.
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from typing import List, Optional


class EmailService:
    """
    Service for sending transactional emails.
    Supports HTML templates with fallback to plain text.
    """

    def __init__(self):
        self.from_email = settings.DEFAULT_FROM_EMAIL

    def send_email(
            self,
            subject: str,
            to_emails: List[str],
            template_name: str,
            context: dict,
            cc_emails: Optional[List[str]] = None,
            bcc_emails: Optional[List[str]] = None,
    ) -> bool:
        """
        Send email using template.

        Args:
            subject: Email subject
            to_emails: List of recipient emails
            template_name: Template name (without extension)
            context: Template context data
            cc_emails: CC recipients (optional)
            bcc_emails: BCC recipients (optional)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Render HTML content
            html_content = render_to_string(
                f'emails/{template_name}.html',
                context
            )

            # Render plain text content
            text_content = render_to_string(
                f'emails/{template_name}.txt',
                context
            )

            # Create email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=to_emails,
                cc=cc_emails,
                bcc=bcc_emails,
            )

            # Attach HTML version
            email.attach_alternative(html_content, "text/html")

            # Send email
            email.send(fail_silently=False)

            return True

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_order_confirmation(self, order):
        """Send order confirmation email to customer."""
        subject = f"Order Confirmation - #{order.order_number}"

        context = {
            'order': order,
            'customer_name': order.customer_name,
            'order_url': f"{settings.SITE_URL}/orders/{order.id}/",
        }

        return self.send_email(
            subject=subject,
            to_emails=[order.customer_email],
            template_name='order_confirmation',
            context=context
        )

    def send_order_status_update(self, order):
        """Send order status update email."""
        subject = f"Order Status Update - #{order.order_number}"

        status_messages = {
            'accepted': 'Your order has been accepted and is being processed.',
            'packed': 'Your order has been packed and ready for delivery.',
            'on_the_way': 'Your order is on the way! ',
            'delivered': 'Your order has been delivered.  Thank you!',
            'cancelled': 'Your order has been cancelled.',
        }

        context = {
            'order': order,
            'status_message': status_messages.get(order.status, ''),
            'order_url': f"{settings.SITE_URL}/orders/{order.id}/",
        }

        return self.send_email(
            subject=subject,
            to_emails=[order.customer_email],
            template_name='order_status_update',
            context=context
        )

    def send_payment_confirmation(self, payment):
        """Send payment confirmation email."""
        subject = f"Payment Confirmation - {payment.payment_id}"

        context = {
            'payment': payment,
            'order': payment.order,
        }

        return self.send_email(
            subject=subject,
            to_emails=[payment.order.customer_email],
            template_name='payment_confirmation',
            context=context
        )

    def send_welcome_email(self, user):
        """Send welcome email to new users."""
        subject = "Welcome to Market!"

        context = {
            'user': user,
            'site_url': settings.SITE_URL,
        }

        return self.send_email(
            subject=subject,
            to_emails=[user.email],
            template_name='welcome',
            context=context
        )