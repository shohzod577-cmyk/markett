"""
PDF generation service for Market platform.
Generates professional invoices and receipts.
"""
from io import BytesIO
from decimal import Decimal
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

from django.conf import settings


class PDFInvoiceGenerator:
    """
    Generate professional PDF invoices for orders.
    """

    def __init__(self, order):
        self.order = order
        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )
        self.styles = getSampleStyleSheet()
        self.story = []

        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12
        )

    def generate(self) -> BytesIO:
        """
        Generate complete invoice PDF.
        Returns BytesIO buffer containing PDF data.
        """
        self._add_header()
        self._add_company_info()
        self._add_invoice_details()
        self._add_customer_info()
        self._add_items_table()
        self._add_totals()
        self._add_payment_info()
        self._add_footer()

        self.doc.build(self.story)
        self.buffer.seek(0)
        return self.buffer

    def _add_header(self):
        """Add invoice header with logo and title."""
        title = Paragraph("INVOICE", self.title_style)
        self.story.append(title)
        self.story.append(Spacer(1, 0.5 * cm))

    def _add_company_info(self):
        """Add company information."""
        company_info = [
            ["<b>MARKET</b>"],
            ["Tashkent, Uzbekistan"],
            ["Email: info@market.uz"],
            ["Phone: +998 71 123 45 67"],
            ["Website: www.market.uz"],
        ]

        table = Table(company_info, colWidths=[18 * cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
        ]))

        self.story.append(table)
        self.story.append(Spacer(1, 1 * cm))

    def _add_invoice_details(self):
        """Add invoice number and date."""
        invoice_data = [
            ['Invoice Number:', self.order.order_number],
            ['Invoice Date:', self.order.created_at.strftime('%d %B %Y')],
            ['Payment Status:', 'PAID' if self.order.is_paid else 'UNPAID'],
            ['Order Status:', self.order.get_status_display()],
        ]

        table = Table(invoice_data, colWidths=[5 * cm, 13 * cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        self.story.append(table)
        self.story.append(Spacer(1, 1 * cm))

    def _add_customer_info(self):
        """Add customer billing and shipping information."""
        heading = Paragraph("BILL TO:", self.heading_style)
        self.story.append(heading)

        customer_data = [
            ['Name:', self.order.customer_name],
            ['Email:', self.order.customer_email],
            ['Phone:', self.order.customer_phone],
            ['Address:', self.order.delivery_address],
            ['City:', self.order.delivery_city],
        ]

        table = Table(customer_data, colWidths=[4 * cm, 14 * cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        self.story.append(table)
        self.story.append(Spacer(1, 1 * cm))

    def _add_items_table(self):
        """Add order items table."""
        heading = Paragraph("ORDER ITEMS:", self.heading_style)
        self.story.append(heading)

        data = [
            ['#', 'Product', 'SKU', 'Qty', 'Unit Price', 'Subtotal']
        ]

        for idx, item in enumerate(self.order.items.all(), 1):
            data.append([
                str(idx),
                item.product_name,
                item.product_sku,
                str(item.quantity),
                f"{item.unit_price:,.2f} {self.order.currency}",
                f"{item.subtotal:,.2f} {self.order.currency}",
            ])

        table = Table(data, colWidths=[1 * cm, 7 * cm, 3 * cm, 2 * cm, 3 * cm, 3 * cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),
            ('ALIGN', (4, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2C3E50')),

            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
        ]))

        self.story.append(table)
        self.story.append(Spacer(1, 0.5 * cm))

    def _add_totals(self):
        """Add order totals section."""
        totals_data = [
            ['Subtotal:', f"{self.order.subtotal:,.2f} {self.order.currency}"],
            ['Delivery Fee:', f"{self.order.delivery_fee:,.2f} {self.order.currency}"],
            ['Tax:', f"{self.order.tax_amount:,.2f} {self.order.currency}"],
            ['Discount:', f"-{self.order.discount_amount:,.2f} {self.order.currency}"],
        ]

        totals_data.append([
            '<b>TOTAL: </b>',
            f"<b>{self.order.total_amount:,.2f} {self.order.currency}</b>"
        ])

        table = Table(totals_data, colWidths=[12 * cm, 6 * cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#3498DB')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#EAF2F8')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
        ]))

        self.story.append(table)
        self.story.append(Spacer(1, 1 * cm))

    def _add_payment_info(self):
        """Add payment information."""
        heading = Paragraph("PAYMENT INFORMATION:", self.heading_style)
        self.story.append(heading)

        payment_method_display = dict(self.order._meta.get_field('payment_method').choices)
        method = payment_method_display.get(self.order.payment_method, self.order.payment_method)

        payment_data = [
            ['Payment Method:', method],
            ['Payment Status:', 'PAID' if self.order.is_paid else 'PENDING'],
        ]

        if self.order.is_paid and self.order.paid_at:
            payment_data.append(['Paid At:', self.order.paid_at.strftime('%d %B %Y %H:%M')])

        table = Table(payment_data, colWidths=[5 * cm, 13 * cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        self.story.append(table)
        self.story.append(Spacer(1, 1 * cm))

    def _add_footer(self):
        """Add invoice footer."""
        footer_text = """
        <para align=center>
        <b>Thank you for your business!</b><br/>
        For any questions regarding this invoice, please contact us at support@market.uz<br/>
        <br/>
        <i>This is a computer-generated invoice and does not require a signature.</i>
        </para>
        """

        footer = Paragraph(footer_text, self.styles['Normal'])
        self.story.append(footer)


class ReceiptGenerator:
    """
    Generate simple receipt for quick reference.
    Lighter alternative to full invoice.
    """

    def __init__(self, order):
        self.order = order

    def generate_text_receipt(self) -> str:
        """
        Generate plain text receipt.
        Useful for SMS or email.
        """
        receipt = f"""
========================================
           MARKET RECEIPT
========================================

Order Number: {self.order.order_number}
Date: {self.order.created_at.strftime('%d/%m/%Y %H:%M')}

Customer: {self.order.customer_name}
Phone: {self.order.customer_phone}

----------------------------------------
ITEMS: 
----------------------------------------
"""

        for idx, item in enumerate(self.order.items.all(), 1):
            receipt += f"{idx}. {item.product_name}\n"
            receipt += f"   Qty: {item.quantity} x {item.unit_price:,.2f} = {item.subtotal:,.2f} {self.order.currency}\n\n"

        receipt += f"""----------------------------------------
Subtotal:      {self.order.subtotal:,.2f} {self.order.currency}
Delivery:     {self.order.delivery_fee:,.2f} {self.order.currency}
Discount:    -{self.order.discount_amount:,.2f} {self.order.currency}
----------------------------------------
TOTAL:        {self.order.total_amount:,.2f} {self.order.currency}
----------------------------------------

Payment:  {self.order.get_payment_method_display()}
Status: {'PAID' if self.order.is_paid else 'PENDING'}

========================================
     Thank you for shopping with us!
========================================
"""
        return receipt