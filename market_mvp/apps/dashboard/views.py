from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.core.mail import send_mail
from django.conf import settings

from apps.orders.models import OrderAction

from apps.orders.models import Order
from apps.products.models import Product
from apps.payments.models import Transaction

@staff_member_required
def home(request):
    User = get_user_model()
    stats = {
        'users_count': User.objects.count(),
        'products_count': Product.objects.count(),
        'orders_count': Order.objects.count(),
        'orders_pending': Order.objects.filter(status=Order.STATUS_PENDING).count(),
        'transactions_count': Transaction.objects.count(),
        'transactions_success': Transaction.objects.filter(status=Transaction.STATUS_SUCCESS).count(),
    }
    recent_orders = Order.objects.order_by('-created_at')[:10]
    return render(request, 'dashboard/home.html', {'stats': stats, 'recent_orders': recent_orders})

@staff_member_required
def stats(request):
    today = timezone.now().date()
    start = today - timezone.timedelta(days=29)
    qs = (
        Order.objects.filter(created_at__date__gte=start)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(orders=Count('id'), revenue=Sum('total'))
        .order_by('day')
    )

    labels = []
    orders_data = []
    revenue_data = []
    days_map = {item['day'].isoformat(): item for item in qs}
    for i in range(30):
        d = start + timezone.timedelta(days=i)
        s = d.isoformat()
        labels.append(s)
        item = days_map.get(s)
        if item:
            orders_data.append(item['orders'] or 0)
            revenue_data.append(float(item['revenue'] or 0))
        else:
            orders_data.append(0)
            revenue_data.append(0.0)

    return JsonResponse({'labels': labels, 'orders': orders_data, 'revenue': revenue_data})


@staff_member_required
def order_action(request, pk, action):
    order = get_object_or_404(Order, pk=pk)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'POST required'}, status=400)

    if action == 'ship':
        if order.status in (Order.STATUS_PAID, Order.STATUS_PROCESSING):
            order.status = Order.STATUS_SHIPPED
            order.save()
            OrderAction.objects.create(order=order, action=OrderAction.ACTION_SHIP, performed_by=request.user)
            try:
                send_mail(
                    subject=f"Your order #{order.id} has shipped",
                    message=f"Hello {order.first_name},\n\nYour order #{order.id} has been marked as shipped.",
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@market.local'),
                    recipient_list=[order.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            return JsonResponse({'ok': True, 'status': order.status})
        return JsonResponse({'ok': False, 'error': 'invalid status for ship'}, status=400)

    if action == 'cancel':
        if order.status not in (Order.STATUS_SHIPPED, Order.STATUS_COMPLETED):
            order.status = Order.STATUS_CANCELED
            order.save()
            OrderAction.objects.create(order=order, action=OrderAction.ACTION_CANCEL, performed_by=request.user)
            try:
                send_mail(
                    subject=f"Your order #{order.id} was canceled",
                    message=f"Hello {order.first_name},\n\nYour order #{order.id} has been canceled.",
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@market.local'),
                    recipient_list=[order.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            return JsonResponse({'ok': True, 'status': order.status})
        return JsonResponse({'ok': False, 'error': 'cannot cancel shipped/completed order'}, status=400)

    return JsonResponse({'ok': False, 'error': 'unknown action'}, status=400)
