from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.views.decorators.cache import cache_control
from django.contrib import messages

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:dashboard')
        return redirect(login)
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

def brands(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'cus_admin/page-brands.html')
    else:
         return redirect('admin_app:admin_login')
        
def order(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'cus_admin/page-orders-1.html')
    else:
         return redirect('admin_app:admin_login')
def order_edit(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'cus_admin/page-orders-detail.html')
    else:
         return redirect('admin_app:admin_login' )


