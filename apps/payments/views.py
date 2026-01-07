"""
Payment processing views.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .models import Payment, Transaction
from .services import PaymentService
from apps.orders.models import Order


@login_required
def payment_process_view(request, order_id):
    """
    Process payment for order.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.is_paid:
        messages.info(request, 'This order has already been paid.')
        return redirect('orders:detail', order_id=order.id)

    # Create payment
    payment_service = PaymentService()
    payment = payment_service.create_payment(
        order=order,
        user=request.user,
        gateway=order.payment_method,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )

    # For cash payment, just confirm
    if order.payment_method == 'cash':
        messages.success(request, 'Order confirmed!  Payment will be collected on delivery.')
        return redirect('orders:detail', order_id=order.id)

    # For online payments, redirect to gateway
    payment_result = payment_service.initiate_payment(payment)

    if payment_result.get('success'):
        return redirect(payment_result['payment_url'])
    else:
        messages.error(request, f"Payment initialization failed: {payment_result.get('error')}")
        return redirect('orders: detail', order_id=order.id)


@login_required
def payment_success_view(request):
    """
    Payment success callback.
    """
    payment_id = request.GET.get('payment_id')

    if payment_id:
        try:
            payment = Payment.objects.get(payment_id=payment_id, user=request.user)

            # Verify payment with gateway
            payment_service = PaymentService()
            verification = payment_service.verify_payment(payment)

            if verification['is_successful']:
                messages.success(request, 'Payment completed successfully!')

                # Send confirmation email
                from core.services.email import EmailService
                EmailService().send_payment_confirmation(payment)
            else:
                messages.warning(request, 'Payment verification pending.  Please check back later.')

            return redirect('orders:detail', order_id=payment.order.id)

        except Payment.DoesNotExist:
            messages.error(request, 'Payment not found.')

    return redirect('orders:list')


@login_required
def payment_cancel_view(request):
    """
    Payment cancelled callback.
    """
    payment_id = request.GET.get('payment_id')

    if payment_id:
        try:
            payment = Payment.objects.get(payment_id=payment_id, user=request.user)
            payment.status = Payment.STATUS_CANCELLED
            payment.save()

            messages.info(request, 'Payment was cancelled.')
            return redirect('orders:detail', order_id=payment.order.id)

        except Payment.DoesNotExist:
            pass

    messages.error(request, 'Invalid payment.')
    return redirect('orders:list')


@csrf_exempt
@require_http_methods(["POST"])
def click_webhook_view(request):
    """
    Click payment gateway webhook handler.
    """
    try:
        # Parse request data
        if request.content_type == 'application/json':
            payload = json.loads(request.body)
        else:
            payload = request.POST.dict()

        # Process webhook
        from .gateways.click import ClickPaymentGateway
        gateway = ClickPaymentGateway()
        response = gateway.handle_webhook(payload, dict(request.headers))

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({
            'error': -1,
            'error_note': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def payme_webhook_view(request):
    """
    Payme payment gateway webhook handler.
    """
    try:
        # Parse JSON-RPC request
        payload = json.loads(request.body)

        # Process webhook
        from .gateways.payme import PaymePaymentGateway
        gateway = PaymePaymentGateway()
        response = gateway.handle_webhook(payload, dict(request.headers))

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({
            "jsonrpc": "2.0",
            "error": {
                "code": -32700,
                "message": "Parse error"
            },
            "id": None
        }, status=500)