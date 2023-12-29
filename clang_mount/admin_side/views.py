from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
# from order.forms import OrderStatusForm
from admin_side.models import User
from django.contrib import messages
from order.models import Order,OrderProduct,Payment
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import ExtractMonth,ExtractWeekDay,ExtractYear

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            return redirect('admin_app:dashboard')
        return redirect('admin_app:admin_login')
        
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        admin = authenticate(email=email, password=password)
        if admin is not None and admin.is_superuser:
            auth_login(request,admin)
            return redirect('admin_app:dashboard')
        else:
            messages.warning(request,'wrong credentials !')
            return redirect('admin_app:admin_login')
    return render(request,'cus_admin/page-account-login.html')

def logout(request):
    auth_logout(request)
    return redirect('admin_app:admin_login')

cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:

            current_date = timezone.now() - timedelta(days=10)
            login_date = timezone.now() - timedelta(days=10)
            total_revenue = Payment.objects.filter(status='SUCCESS').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
            orders_count = Order.objects.filter(Q(is_ordered=True)).aggregate(Count('id'))['id__count'] or 0
            product_count = OrderProduct.objects.filter(Q(order__payment__status='SUCCESS') & Q(status='DELIVERED')).aggregate(Sum('quantity'))['quantity__sum'] or 0
            monthly_sales = Payment.objects.filter(created_at__month=timezone.now().month,status="SUCCESS").aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
            yearly_sales = Payment.objects.filter(created_at__year=timezone.now().year,status="SUCCESS").aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
            user = User.objects.filter(is_active=True).count()
            new_member = User.objects.filter(joined_on__date__gt =current_date)
            last_login = User.objects.filter(last_login__date__lt = login_date)
            orders = Order.objects.filter(is_ordered=True)
            
            
            weekly_sales_data = get_weekly_sales()
            monthly_sales_data = get_monthly_sales()
            yearly_sales_data = get_yearly_sales()

            # Convert data to string for use in JavaScript
            weekly_sales_str = ",".join(map(str, weekly_sales_data))
            monthly_sales_str = ",".join(map(str, monthly_sales_data))
            yearly_sales_str = ",".join(map(str, yearly_sales_data))

            print(weekly_sales_str)

            context = {
                'revenue': total_revenue,
                'orders_count':orders_count,
                'product_count':product_count,
                'weekly_sales_data': weekly_sales_str,
                'monthly_sales_data': monthly_sales_str,
                'yearly_sales_data': yearly_sales_str,
                'monthly_sales': monthly_sales,
                'yearly_sales': yearly_sales,
                'orders':orders,
                'user': user,
                'new_members': new_member,
                'last_logins': last_login,

            }
            return render(request,'cus_admin/index.html',context)
    return redirect('admin_app:admin_login')

def get_weekly_sales():
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    print(start_of_week,'\n',end_of_week)
    weekly_sales = Payment.objects.filter(
        created_at__date__range=[start_of_week, end_of_week],
        status="SUCCESS"
    ).annotate(day_of_week=ExtractWeekDay('created_at')).values('day_of_week').annotate(weekly_total=Sum('amount_paid')).order_by('day_of_week')
    print(weekly_sales)
    weekly_sales_values = [0] * 7
    for entry in weekly_sales:

        adjusted_index = entry['day_of_week'] - 2
        weekly_sales_values[adjusted_index] = entry['weekly_total']

    return weekly_sales_values

def get_monthly_sales():
    # Query to get monthly sales for the current year
    monthly_sales = Payment.objects.filter(
        created_at__year=timezone.now().year,
        status="SUCCESS"
    ).annotate(month=ExtractMonth('created_at')).values('month').annotate(monthly_total=Sum('amount_paid')).order_by('month')

    monthly_sales_values = [0] * 12

    for entry in monthly_sales:
        month_index = entry['month'] - 1
        monthly_sales_values[month_index] = entry['monthly_total']

    return monthly_sales_values

def get_yearly_sales():
    yearly_sales = Payment.objects.filter(
        created_at__year=timezone.now().year,
        status="SUCCESS"
    ).annotate(year=ExtractYear('created_at')).values('year').annotate(yearly_total=Sum('amount_paid')).order_by('year')

    yearly_sales_values = [0] * 12  # Assuming you want data for each month in a year
    for entry in yearly_sales:
        year_index = entry['year'] - timezone.now().year  # Adjust to get a 0-based index
        yearly_sales_values[year_index] = entry['yearly_total']

    return yearly_sales_values


def order(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.all().order_by('-created_at').filter(is_ordered=True)
        for order in orders:
            order.delivery_date = order.payment.created_at.date() + timedelta(days=3)
        context = {
            'orders': orders,
        }
        return render(request,'cus_admin/page-orders.html',context)
    else:
         return redirect('admin_app:admin_login')
    
def order_details(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=id)
        order_products = OrderProduct.objects.filter(order=order)

        context = {
            'order': order,
            'order_products': order_products,
        }
        
        return render(request,'cus_admin/page-orders-details.html',context)
    else:
         return redirect('admin_app:admin_login' )

def order_status(request):
    
    if request.POST.get('action') == 'POST':
        status = request.POST.get('status')
        id = request.POST.get('id')
        order_product = OrderProduct.objects.get(id=id)
        order_product.status = status
        order_product.save()
        if order_product.status == 'DELIVERED':
            order.payment.status = 'SUCCESS'
            order.payment.save()
        return JsonResponse({'success':True})
    else:
        messages.success(request,'Failed')
        return redirect('admin_app:order')

def search(request):
    query = request.POST.get('search')

    if query:
        orders = Order.objects.filter(
            Q(order_no__icontains=query) |
            Q(user__username__icontains=query) 
        )
    else:
        return redirect('admin_app:order')
    context = {
        'orders': orders,
    }
    return render(request,'cus_admin/page-orders.html',context)
