"""
Order management views. 
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .models import Order, OrderItem
from .forms import CheckoutForm
from .services import OrderService
from apps.cart.services import CartService
from core.services.pdf import PDFInvoiceGenerator


@login_required
def checkout_view(request):
    """
    Multi-step checkout process.
    """
    cart_service = CartService(request.user)
    cart = cart_service.get_cart()

    if not cart or cart.items_count == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:view')

    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            # Get currency from session
            currency = request.session.get('currency', 'UZS')

            # Create order
            order_service = OrderService()
            order = order_service.create_order_from_cart(
                user=request.user,
                cart=cart,
                checkout_data=form.cleaned_data,
                currency=currency
            )

            # Clear cart
            cart_service.clear_cart()

            # Send confirmation email
            from core.services.email import EmailService
            EmailService().send_order_confirmation(order)

            messages.success(request, f'Order #{order.order_number} placed successfully!')

            # Redirect to payment if not cash
            if order.payment_method != 'cash':
                return redirect('payments:process', order_id=order.id)

            return redirect('orders:detail', order_id=order.id)
    else:
        # Pre-fill form with user data
        initial_data = {
            'customer_name': request.user.get_full_name,
            'customer_email': request.user.email,
            'customer_phone': request.user.phone,
        }
        form = CheckoutForm(initial=initial_data, user=request.user)

    # Calculate total
    currency = request.session.get('currency', 'UZS')
    total = cart.get_total(currency)

    context = {
        'form': form,
        'cart': cart,
        'total': total,
        'currency': currency,
    }

    return render(request, 'orders/checkout.html', context)


@login_required
def order_list_view(request):
    """
    Display user's order history.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
    }

    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail_view(request, order_id):
    """
    Display order details. 
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        'order': order,
    }

    return render(request, 'orders/order_detail.html', context)


@login_required
def cancel_order_view(request, order_id):
    """
    Cancel order (if allowed).
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        reason = request.POST.get('reason', 'Customer request')

        try:
            order.cancel(user=request.user, reason=reason)
            messages.success(request, 'Order cancelled successfully.')
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('orders:detail', order_id=order.id)

    return render(request, 'orders/cancel_order.html', {'order': order})


@login_required
def download_invoice_view(request, order_id):
    """
    Download order invoice as PDF.
    """
    from django.http import HttpResponse

    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Generate PDF
    pdf_generator = PDFInvoiceGenerator(order)
    pdf_buffer = pdf_generator.generate()

    # Return as download
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_number}.pdf"'

    return response