from django.shortcuts import render, HttpResponse,redirect
from order.models import Order, OrderProduct, Payment
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from openpyxl import Workbook
# Create your views here.


def sales_report(request):
    if request.user.is_authenticated and request.user.is_superuser:
        order_product = OrderProduct.objects.filter(is_ordered = True).order_by('-created_at')
        context = {
            'order_product':order_product,
        }
        return render(request,'cus_admin/page-sales-report.html',context)
    else:
        return redirect('admin_app:admin_login')
    

def sales_report_pdf(request):
    
    orders = Order.objects.filter(status='DELIVERED')

    buffer = io.BytesIO()

    # Create a PDF object using the SimpleDocTemplate
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    table_header = ["Order ID","user name", "Product", "Quantity", "Price","Payment Method","Order Status"]
    elements.append(table_header)

    order_products = OrderProduct.objects.filter(is_ordered=True)
    for product in order_products:
        product_info = [
            product.order.order_no,
            product.order.user.first_name,
            product.product.product_name,
            str(product.quantity),
            str(product.product_price),
            product.order.payment.payment_method,
            product.order.status,
        ]
        elements.append(product_info)

    table = Table(elements)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#4285f4'),
                               ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1, 1)),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), '#eeeeee'),
                               ]))
    elements = [table]

    doc.build(elements)

    # Move the buffer's cursor to the beginning
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="sales_report.pdf")


def sales_report_excel(request):
    
    order_products = OrderProduct.objects.filter(is_ordered=True)

    # Create a response object with Excel mime type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sales_report.xlsx'

    # Create an Excel workbook and add a worksheet
    workbook = Workbook()
    worksheet = workbook.active

    
    table_header = ["Order ID", "User Name", "Product", "Quantity", "Price", "Payment Method", "Order Status"]
    worksheet.append(table_header)

   
    for product in order_products:
        product_info = [
            product.order.order_no,
            product.order.user.first_name,
            str(product.product.product_name),
            str(product.quantity),
            str(product.product_price),
            product.order.payment.payment_method,
            product.order.status,
        ]
        worksheet.append(product_info)

    workbook.save(response)

    return response
