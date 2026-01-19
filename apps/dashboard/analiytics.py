"""
Dashboard analytics service.
Business intelligence and metrics calculation.
"""
from django.db.models import Sum, Count, Avg, Q, F
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from apps.orders.models import Order
from apps.products.models import Product
from apps.users.models import User
from apps.payments.models import Payment


class DashboardAnalytics:
    """
    Service for calculating dashboard metrics and analytics.
    """

    def get_overview_metrics(self):
        """
        Get high-level overview metrics.
        """
        return {
            'total_users': User.objects.count(),
            'total_products': Product.objects.filter(is_active=True).count(),
            'total_orders': Order.objects.count(),
            'total_revenue': self._get_total_revenue(),
            'pending_orders': Order.objects.filter(status=Order.STATUS_PENDING).count(),
            'unpaid_orders': Order.objects.filter(is_paid=False).exclude(status=Order.STATUS_CANCELLED).count(),
            'low_stock_products': Product.objects.filter(is_active=True, stock__lt=10).count(),
        }

    def get_revenue_metrics(self, days=30):
        """
        Get revenue metrics for specified period.
        """
        date_from = timezone.now() - timedelta(days=days)

        current_period = Order.objects.filter(
            created_at__gte=date_from,
            is_paid=True
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )

        previous_period = Order.objects.filter(
            created_at__gte=date_from - timedelta(days=days),
            created_at__lt=date_from,
            is_paid=True
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )

        current_total = current_period['total'] or 0
        previous_total = previous_period['total'] or 0

        change_percent = 0
        if previous_total > 0:
            change_percent = ((current_total - previous_total) / previous_total) * 100

        return {
            'current_revenue': current_total,
            'previous_revenue': previous_total,
            'change_percent': round(change_percent, 2),
            'order_count': current_period['count'],
        }

    def get_order_metrics(self, days=30):
        """
        Get order metrics.
        """
        date_from = timezone.now() - timedelta(days=days)

        orders = Order.objects.filter(created_at__gte=date_from)

        return {
            'total_orders': orders.count(),
            'pending': orders.filter(status=Order.STATUS_PENDING).count(),
            'accepted': orders.filter(status=Order.STATUS_ACCEPTED).count(),
            'on_the_way': orders.filter(status=Order.STATUS_ON_THE_WAY).count(),
            'delivered': orders.filter(status=Order.STATUS_DELIVERED).count(),
            'cancelled': orders.filter(status=Order.STATUS_CANCELLED).count(),
        }

    def get_product_metrics(self):
        """
        Get product metrics.
        """
        return {
            'total_products': Product.objects.filter(is_active=True).count(),
            'out_of_stock': Product.objects.filter(is_active=True, stock=0).count(),
            'low_stock': Product.objects.filter(is_active=True, stock__gt=0, stock__lt=10).count(),
            'featured': Product.objects.filter(is_active=True, is_featured=True).count(),
        }

    def get_top_products(self, limit=10):
        """
        Get top-selling products.
        """
        return Product.objects.filter(
            is_active=True
        ).order_by('-sales_count')[:limit]

    def get_chart_data(self, days=30):
        """
        Get data for dashboard charts.
        """
        date_from = timezone.now() - timedelta(days=days)

        daily_revenue = Order.objects.filter(
            created_at__gte=date_from,
            is_paid=True
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            revenue=Sum('total_amount')
        ).order_by('date')

        daily_orders = Order.objects.filter(
            created_at__gte=date_from
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        return {
            'revenue': list(daily_revenue),
            'orders': list(daily_orders),
        }

    def get_revenue_chart_data(self, days=30):
        """
        Get revenue chart data for AJAX.
        """
        date_from = timezone.now() - timedelta(days=days)

        data = Order.objects.filter(
            created_at__gte=date_from,
            is_paid=True
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            revenue=Sum('total_amount')
        ).order_by('date')

        return {
            'labels': [item['date'].strftime('%Y-%m-%d') for item in data],
            'data': [float(item['revenue']) for item in data],
        }

    def get_orders_chart_data(self, days=30):
        """
        Get orders chart data for AJAX.
        """
        date_from = timezone.now() - timedelta(days=days)

        data = Order.objects.filter(
            created_at__gte=date_from
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        return {
            'labels': [item['date'].strftime('%Y-%m-%d') for item in data],
            'data': [item['count'] for item in data],
        }

    def get_users_chart_data(self, days=30):
        """
        Get new users chart data for AJAX.
        """
        date_from = timezone.now() - timedelta(days=days)

        data = User.objects.filter(
            created_at__gte=date_from
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        return {
            'labels': [item['date'].strftime('%Y-%m-%d') for item in data],
            'data': [item['count'] for item in data],
        }

    def _get_total_revenue(self):
        """
        Calculate total revenue from paid orders.
        """
        total = Order.objects.filter(is_paid=True).aggregate(Sum('total_amount'))
        return total['total_amount__sum'] or Decimal('0')

    def get_sold_products_metrics(self):
        """
        Get metrics about sold products.
        Returns total quantity of products sold and number of unique products sold.
        """
        from apps.orders.models import OrderItem
        
        sold_quantity = OrderItem.objects.filter(
            order__is_paid=True
        ).aggregate(
            total=Sum('quantity')
        )['total'] or 0
        
        unique_products_sold = OrderItem.objects.filter(
            order__is_paid=True
        ).values('product').distinct().count()
        
        sold_value = OrderItem.objects.filter(
            order__is_paid=True
        ).aggregate(
            total=Sum(F('unit_price') * F('quantity'))
        )['total'] or Decimal('0')
        
        return {
            'total_sold_quantity': sold_quantity,
            'unique_products_sold': unique_products_sold,
            'sold_value': sold_value,
        }
    
    def get_remaining_products_metrics(self):
        """
        Get metrics about remaining (unsold) products in stock.
        Returns total quantity in stock and total value.
        """
        remaining_quantity = Product.objects.filter(
            is_active=True
        ).aggregate(
            total=Sum('stock')
        )['total'] or 0
        
        remaining_value = Product.objects.filter(
            is_active=True
        ).aggregate(
            total=Sum(F('price') * F('stock'))
        )['total'] or Decimal('0')
        
        products_in_stock = Product.objects.filter(
            is_active=True,
            stock__gt=0
        ).count()
        
        return {
            'total_remaining_quantity': remaining_quantity,
            'products_in_stock': products_in_stock,
            'remaining_value': remaining_value,
        }