from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.views.decorators.cache import cache_control
from django.contrib import messages

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(dashboard)
        return redirect(login)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        admin = authenticate(email=email, password=password)
        if admin is not None and admin.is_superuser:
            auth_login(request,admin)
            return redirect(dashboard)
        else:
            messages.warning(request,'wrong credentials !')
            return redirect(login)
    return render(request,'admin/page-account-login.html')
def logout(request):
    auth_logout(request)
    return redirect(login)
cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request,'admin/index.html')
    return redirect(login)
def product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'admin/page-products-list.html')
    else:
        return redirect(login)
def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'admin/page-form-product-3.html')
    else:
         return redirect(login)
def product_edit(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'admin/page-product-detail.html')
    else:
         return redirect(login)
def brands(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'admin/page-brands.html')
    else:
         return redirect(login)
        
def categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'admin/page-categories.html')
    else:
         return redirect(login)
def order(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'admin/page-orders-1.html')
    else:
         return redirect(login)
def order_edit(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'admin/page-orders-detail.html')
    else:
         return redirect(login)
def customer(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'admin/page-customers-list.html')
    else:
         return redirect(login)
def customer_edit(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'admin/page-customers-detail.html')
    else:
         return redirect(login)


