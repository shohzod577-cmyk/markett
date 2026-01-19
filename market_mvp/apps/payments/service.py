from urllib.parse import urlencode

from django.urls import reverse

from .models import Transaction


def initiate_payment(request, order, gateway='click'):
    txn = Transaction.objects.create(
        user=order.user,
        order_id=order.id,
        gateway=gateway,
        amount=order.total,
        currency='UZS',
        status=Transaction.STATUS_PENDING,
    )

    params = urlencode({'txn_id': txn.id})
    redirect_url = reverse('payments:mock_complete', args=[txn.id]) + f'?{params}'
    return {'transaction': txn, 'redirect_url': redirect_url}
