"""
Custom admin dashboard views.
Production-grade admin interface (NOT Django default admin).
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg, Q
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from datetime import datetime, timedelta

from .decorators import admin_required
from .analytics import DashboardAnalytics
from apps.users.models import User
from apps.products.models import Product, Category
from apps.orders.models import Order
from apps.payments.models import Payment
from apps.reviews.models import Review


@login_required
@admin_required
def dashboard_home_view(request):
    """
    Main dashboard with key metrics and analytics.
    """
    analytics = DashboardAnalytics()

    # Get date range from request
    days = int(request.GET.get('days', 30))

    context = {
        'overview': analytics.get_overview_metrics(),
        'revenue': analytics.get_revenue_metrics(days),
        'orders': analytics.get_order_metrics(days),
        'products': analytics.get_product_metrics(),
        'recent_orders': Order.objects.all().order_by('-created_at')[:10],
        'top_products': analytics.get_top_products(limit=5),
        'chart_data': analytics.get_chart_data(days),
    }

    return render(request, 'dashboard/home.html', context)


@login_required
@admin_required
def users_list_view(request):
    """
    User management view.
    """
    users = User.objects.all().order_by('-created_at')

    # Filters
    search = request.GET.get('search', '')
    if search:
        users = users.filter(
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    context = {
        'users': users,
        'search': search,
    }

    return render(request, 'dashboard/users_list.html', context)


@login_required
@admin_required
def user_detail_view(request, user_id):
    """
    User detail and management. 
    """
    user = get_object_or_404(User, id=user_id)

    context = {
        'user': user,
        'orders': user.orders.all()[:20],
        'reviews': user.reviews.all()[:20],
        'total_spent': user.orders.filter(is_paid=True).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
    }

    return render(request, 'dashboard/user_detail.html', context)


@login_required
@admin_required
def block_user_view(request, user_id):
    """
    Block/unblock user.
    """
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        reason = request.POST.get('reason', '')

        user.is_blocked = not user.is_blocked
        if user.is_blocked:
            user.blocked_reason = reason
        else:
            user.blocked_reason = ''

        user.save()

        action = 'blocked' if user.is_blocked else 'unblocked'
        messages.success(request, f'User {user.email} has been {action}.')

        return redirect('dashboard:user_detail', user_id=user.id)

    return redirect('dashboard:users_list')


@login_required
@admin_required
def products_list_view(request):
    """
    Product management view. 
    """
    products = Product.objects.all().select_related('category').order_by('-created_at')

    # Filters
    search = request.GET.get('search', '')
    category_id = request.GET.get('category')
    status = request.GET.get('status')

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(sku__icontains=search) |
            Q(brand__icontains=search)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    if status == 'active':
        products = products.filter(is_active=True)
    elif status == 'inactive':
        products = products.filter(is_active=False)
    elif status == 'low_stock':
        products = products.filter(stock__lt=10)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'search': search,
    }

    return render(request, 'dashboard/products_list.html', context)


@login_required
@admin_required
def orders_list_view(request):
    """
    Order management view. 
    """
    orders = Order.objects.all().select_related('user').order_by('-created_at')

    # Filters
    status = request.GET.get('status')
    payment_status = request.GET.get('payment_status')
    search = request.GET.get('search', '')

    if status:
        orders = orders.filter(status=status)

    if payment_status == 'paid':
        orders = orders.filter(is_paid=True)
    elif payment_status == 'unpaid':
        orders = orders.filter(is_paid=False)

    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(customer_email__icontains=search) |
            Q(customer_phone__icontains=search)
        )

    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'search': search,
    }

    return render(request, 'dashboard/orders_list.html', context)


@login_required
@admin_required
def order_detail_view(request, order_id):
    """
    Order detail and management.
    """
    order = get_object_or_404(Order.objects.select_related('user'), id=order_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_status':
            new_status = request.POST.get('status')
            notes = request.POST.get('notes', '')

            from apps.orders.services import OrderService
            OrderService().update_order_status(
                order=order,
                new_status=new_status,
                user=request.user,
                notes=notes
            )

            messages.success(request, 'Order status updated successfully.')

        return redirect('dashboard:order_detail', order_id=order.id)

    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
        'status_history': order.status_history.all(),
        'payments': order.payments.all(),
    }

    return render(request, 'dashboard/order_detail.html', context)


@login_required
@admin_required
def reviews_list_view(request):
    """
    Review moderation view.
    """
    reviews = Review.objects.all().select_related('user', 'product').order_by('-created_at')

    # Filters
    status = request.GET.get('status')

    if status == 'pending':
        reviews = reviews.filter(is_approved=False, is_flagged=False)
    elif status == 'approved':
        reviews = reviews.filter(is_approved=True)
    elif status == 'flagged':
        reviews = reviews.filter(is_flagged=True)

    context = {
        'reviews': reviews,
    }

    return render(request, 'dashboard/reviews_list.html', context)


@login_required
@admin_required
def review_moderate_view(request, review_id):
    """
    Moderate review (approve/reject/flag).
    """
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        action = request.POST.get('action')

        if action == 'approve':
            review.is_approved = True
            review.is_flagged = False
            messages.success(request, 'Review approved.')
        elif action == 'reject':
            review.is_approved = False
            messages.success(request, 'Review rejected.')
        elif action == 'flag':
            review.is_flagged = True
            review.moderation_notes = request.POST.get('notes', '')
            messages.success(request, 'Review flagged.')

        review.save()

        return redirect('dashboard:reviews_list')

    return redirect('dashboard:reviews_list')


@login_required
@admin_required
def analytics_api_view(request):
    """
    API endpoint for dashboard charts (AJAX).
    """
    metric = request.GET.get('metric', 'revenue')
    days = int(request.GET.get('days', 30))

    analytics = DashboardAnalytics()

    if metric == 'revenue':
        data = analytics.get_revenue_chart_data(days)
    elif metric == 'orders':
        data = analytics.get_orders_chart_data(days)
    elif metric == 'users':
        data = analytics.get_users_chart_data(days)
    else:
        data = {}

    return JsonResponse(data)