import json
import hmac
import hashlib
from decimal import Decimal

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from apps.orders.models import Order
from .models import Transaction
from apps.orders.services import generate_invoice_pdf
from django.core.mail import EmailMessage
from .service import initiate_payment


def _record_webhook(gateway, payload):
    ref = payload.get('order_id') or payload.get('transaction_id') or payload.get('id')
    raw_amount = payload.get('amount') or payload.get('sum') or payload.get('price') or 0
    try:
        amount = Decimal(str(raw_amount))
    except Exception:
        amount = Decimal('0')

    txn = Transaction.objects.create(
        gateway=gateway,
        amount=amount,
        currency=payload.get('currency', 'UZS'),
        status=Transaction.STATUS_PENDING,
        reference=str(ref) if ref else '',
        payload=payload,
    )

    order = None
    try:
        if ref:
            oid = int(ref)
            order = Order.objects.filter(pk=oid).first()
            if order:
                txn.order_id = order.id
                if order.user:
                    txn.user = order.user
                txn.save()
    except Exception:
        order = None

    status_flag = (payload.get('status') or payload.get('state') or '').lower()
    if status_flag in ('success', 'ok', 'completed', 'paid'):
        txn.status = Transaction.STATUS_SUCCESS
        txn.save()
        if order:
            order.status = Order.STATUS_PAID
            order.save()
            try:
                pdf_bytes = generate_invoice_pdf(order)
                email = EmailMessage(
                    subject=f"Order #{order.id} confirmed",
                    body=f"Thank you. Your order #{order.id} has been paid.",
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@market.local'),
                    to=[order.email],
                )
                email.attach(f"invoice_order_{order.id}.pdf", pdf_bytes, 'application/pdf')
                email.send(fail_silently=True)
            except Exception:
                pass
    return txn


def _verify_signature(request, header_name, secret_value):
    if not secret_value:
        return True
    sig = request.headers.get(header_name)
    if not sig:
        return False
    try:
        mac = hmac.new(secret_value.encode('utf-8'), request.body or b'', hashlib.sha256).hexdigest()
    except Exception:
        return False
    return hmac.compare_digest(mac, sig)


@csrf_exempt
def click_webhook(request):
    if getattr(settings, 'PAYMENT_VERIFY_ENABLED', True):
        secret = getattr(settings, 'PAYMENT_CLICK_SECRET', '')
        if not _verify_signature(request, 'X-Click-Signature', secret):
            return HttpResponseForbidden('invalid signature')
    try:
        payload = json.loads(request.body)
    except Exception:
        return HttpResponseBadRequest('invalid json')

    txn = _record_webhook('click', payload)
    return JsonResponse({'status': 'ok', 'txn_id': txn.id})


@csrf_exempt
def payme_webhook(request):
    if getattr(settings, 'PAYMENT_VERIFY_ENABLED', True):
        secret = getattr(settings, 'PAYMENT_PAYME_SECRET', '')
        if not _verify_signature(request, 'X-Payme-Signature', secret):
            return HttpResponseForbidden('invalid signature')
    try:
        payload = json.loads(request.body)
    except Exception:
        return HttpResponseBadRequest('invalid json')

    txn = _record_webhook('payme', payload)
    return JsonResponse({'result': 'ok', 'txn_id': txn.id})


@csrf_exempt
def uzum_webhook(request):
    if getattr(settings, 'PAYMENT_VERIFY_ENABLED', True):
        secret = getattr(settings, 'PAYMENT_UZUM_SECRET', '')
        if not _verify_signature(request, 'X-Uzum-Signature', secret):
            return HttpResponseForbidden('invalid signature')
    try:
        payload = json.loads(request.body)
    except Exception:
        return HttpResponseBadRequest('invalid json')

    txn = _record_webhook('uzum', payload)
    return JsonResponse({'ok': True, 'txn_id': txn.id})


def initiate(request, order_id, gateway='click'):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return HttpResponseBadRequest('order not found')

    result = initiate_payment(request, order, gateway=gateway)
    return JsonResponse({'redirect': result['redirect_url'], 'txn_id': result['transaction'].id})


def mock_complete(request, txn_id):
    try:
        txn = Transaction.objects.get(pk=txn_id)
    except Transaction.DoesNotExist:
        return HttpResponseBadRequest('txn not found')

    txn.status = Transaction.STATUS_SUCCESS
    txn.save()

    if txn.order_id:
        try:
            order = Order.objects.get(pk=txn.order_id)
            order.status = Order.STATUS_PAID
            order.save()
        except Order.DoesNotExist:
            pass

    return JsonResponse({'ok': True, 'txn_id': txn.id, 'status': txn.status})
