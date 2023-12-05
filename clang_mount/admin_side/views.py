from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.views.decorators.cache import cache_control
from django.db.models import Q
from order.forms import OrderStatusForm
from django.contrib import messages
from order.models import Order,OrderProduct

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
            return render(request,'cus_admin/index.html')
    return redirect('admin_app:admin_login')

def order(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.all().order_by('-created_at')
        context = {
            'orders': orders,
        }
        return render(request,'cus_admin/page-orders.html',context)
    else:
         return redirect('admin_app:admin_login')
    
def order_details(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=id)
        order_product = OrderProduct.objects.filter(order=order)
        
        if request.method == 'POST':
            form = OrderStatusForm(request.POST,instance=order)
            if form.is_valid():
                form.save()
        else:
            form = OrderStatusForm(instance=order)
            
        context = {
            'order':order,
            'order_product':order_product,
            'form': form,
        }
        
        return render(request,'cus_admin/page-orders-details.html',context)
    else:
         return redirect('admin_app:admin_login' )

def search(request):
    query = request.POST.get('search')

    if query:
        orders = Order.objects.filter(
            Q(order_no__icontains=query) |
            Q(user__user_name__icontains=query) |
            Q(status__icontains=query)
        )
    else:
        return redirect('admin_app:order')
    context = {
        'orders': orders,
    }
    return render(request,'cus_admin/page-orders.html',context)
