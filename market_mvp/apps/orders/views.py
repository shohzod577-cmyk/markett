from django.shortcuts import get_object_or_404, redirect, render

from apps.cart.views import _get_or_create_cart
from .forms import OrderCreateForm
from .models import Order
from .services import generate_invoice_pdf
from django.http import HttpResponse, HttpResponseForbidden


def checkout(request):
    cart = _get_or_create_cart(request)
    if not cart.items.exists():
        return redirect('cart:detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = Order.create_from_cart(cart, form.cleaned_data)
            cart.items.all().delete()
            return redirect('orders:detail', pk=order.pk)
    else:
        form = OrderCreateForm(initial={'email': request.user.email} if request.user.is_authenticated else None)

    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})


def download_invoice(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status != Order.STATUS_PAID and not request.user.is_staff:
        return HttpResponseForbidden('invoice available for paid orders only')

    pdf_bytes = generate_invoice_pdf(order)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_order_{order.id}.pdf"'
    return response
