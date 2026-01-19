from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def generate_invoice_pdf(order):
    """Return PDF bytes for a simple invoice for `order`."""
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    margin = 20 * mm
    x = margin
    y = height - margin

    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, f"Invoice — Order #{order.id}")
    c.setFont("Helvetica", 10)
    y -= 16
    c.drawString(x, y, f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    y -= 20

    c.drawString(x, y, f"Bill To: {order.first_name} {order.last_name}")
    y -= 12
    c.drawString(x, y, f"Email: {order.email}")
    y -= 12
    c.drawString(x, y, f"Address: {order.address_line1} {order.address_line2} {order.city}")
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y, "Items")
    y -= 14
    c.setFont("Helvetica", 10)

    for item in order.items.all():
        line = f"{item.quantity} x {item.product.title} — {item.price}"
        c.drawString(x, y, line)
        y -= 12
        if y < margin + 40:
            c.showPage()
            y = height - margin

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, f"Total: {order.total}")

    c.showPage()
    c.save()

    buf.seek(0)
    return buf.read()
