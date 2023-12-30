from django.shortcuts import render, HttpResponse,redirect
from order.models import Order, OrderProduct, Payment
from django.db.models import Q
import io
from django.http import FileResponse,JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from openpyxl import Workbook
from django.utils import timezone
from datetime import timedelta
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def sales_report(request):
    if request.user.is_authenticated and request.user.is_superuser:
        
        order_product = OrderProduct.objects.filter(is_ordered=True).order_by('-created_at')

        items_per_page = 10
        paginator = Paginator(order_product, items_per_page)
        page = request.GET.get('page')

        try:
            order_product_page = paginator.page(page)
        except PageNotAnInteger:
            order_product_page = paginator.page(1)
        except EmptyPage:
            order_product_page = paginator.page(paginator.num_pages)

        context = {
            'order_product_page': order_product_page,
        }

        return render(request, 'cus_admin/page-sales-report.html', context)
    else:
        return redirect('admin_app:admin_login')
    

def sales_report_pdf(request):
    
    orders = OrderProduct.objects.filter(status='DELIVERED')

    buffer = io.BytesIO()

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
            product.status,
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

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sales_report.xlsx'

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
            product.status,
        ]
        worksheet.append(product_info)

    workbook.save(response)
    return response

def sales_reports_details(request,intervel):
    if request.user.is_authenticated and request.user.is_superuser:
        order_product = None
        today = timezone.now().date()

        if intervel == 'daily':
            order_product = OrderProduct.objects.filter(is_ordered = True,created_at__date = today).order_by('-created_at')

        elif intervel == 'weekly':
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=7)
            order_product = OrderProduct.objects.filter(is_ordered = True,created_at__date__range=[start_of_week,end_of_week]).order_by('-created_at')

        elif intervel =='monthly':
            order_product = OrderProduct.objects.filter(is_ordered = True,created_at__date__month=timezone.now().month ).order_by('created_at')

        elif intervel == 'yearly':
            order_product = OrderProduct.objects.filter(is_ordered = True,created_at__date__year=timezone.now().year ).order_by('created_at')

        items_per_page = 10
        paginator = Paginator(order_product, items_per_page)
        page = request.GET.get('page')

        try:
            order_product_page = paginator.page(page)
        except PageNotAnInteger:
            order_product_page = paginator.page(1)
        except EmptyPage:
            order_product_page = paginator.page(paginator.num_pages)

        context = {
            'order_product_page': order_product_page,
        }

        return render(request,'cus_admin/page-sales-report.html',context)
    else:
        return redirect('admin_app:admin_login')

    
def sales_report_range(request):
    if request.user.is_authenticated and request.user.is_superuser:

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        print(from_date)
        print(to_date)
        products = OrderProduct.objects.filter(is_ordered = True,created_at__date__range=[from_date,to_date]).order_by('-created_at')
        
        items_per_page = 10
        paginator = Paginator(products, items_per_page)
        page = request.GET.get('page')

        try:
            order_product_page = paginator.page(page)
        except PageNotAnInteger:
            order_product_page = paginator.page(1)
        except EmptyPage:
            order_product_page = paginator.page(paginator.num_pages)

        context = {
            'order_product_page': order_product_page,
        }
        
        return render(request,'cus_admin/page-sales-report.html',context)
    else:
        return redirect('admin_app:admin_login')
    

# def sales_report_range(request):
#     if request.user.is_authenticated and request.user.is_superuser:

#         from_date = request.GET.get('from_date')
#         to_date = request.GET.get('to_date')
#         products = OrderProduct.objects.filter(is_ordered = True,created_at__date__range=[from_date,to_date]).order_by('-created_at')
        
#         items_per_page = 10
#         paginator = Paginator(products, items_per_page)
#         page = request.GET.get('page')

#         try:
#             order_product_page = paginator.page(page)
#         except PageNotAnInteger:
#             order_product_page = paginator.page(1)
#         except EmptyPage:
#             order_product_page = paginator.page(paginator.num_pages)

#         order_products = [{'order_id':product.order.order_no,'created_at':product.created_at.date(),'firstname':product.order.user.first_name,
#                            'secondname':product.order.user.last_name,'product':str(product.product.product_name),'quantity':product.quantity,
#                            'price':product.product_price,'payment_method':product.order.payment.payment_method} for product in order_product_page]
        
#         response_data = {
#             'order_product': order_products,
#             'paginator': {
#                 'num_pages': paginator.num_pages,
#                 'current_page': order_product_page.number,
#                 'has_next': order_product_page.has_next(),
#                 'has_previous': order_product_page.has_previous(),
#                 'from_date': from_date,
#                 'to_date':to_date,
#             }
#         }
        
#         return JsonResponse(response_data)
#     else:
#         return redirect('admin_app:admin_login')