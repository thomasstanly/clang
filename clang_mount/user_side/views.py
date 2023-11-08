from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.views.decorators.cache import cache_control
from admin_side.views import login as admin_login
from django.contrib import messages
from admin_side.models import User
from admin_side.views import dashboard

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(dashboard)
        return redirect(index)
    if request.method == "POST":
        user = request.POST["username"]
        email = request.POST["email"]
        passw = request.POST["password"]
        conpass = request.POST["conf_password"]
        try:
                if User.objects.get(email = email):
                    messages.warning(request,"email  is taken")
                    return redirect(signup)
        except:
                pass
        if user != " ":
            messages.info(request,"Password minimum 8 characters")
            return redirect(signup)
        if passw != conpass:
            messages.warning(request,"Password is incorrect")
            return redirect(signup)
        if len(passw) < 8:
            messages.info(request,"Password minimum 8 characters")
            return redirect(signup)
        user_details = User.objects.create_user(email = email, user_name = user, password = passw)
        user_details.save()
        return redirect(login)
    return render(request,'user/page-login-register.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(admin_login)
        return redirect(index)
    if request.method == "POST":
        email = request.POST["email"]
        passw = request.POST["password"]
        user_details = authenticate(email = email,password = passw)
        if user_details is not None and user_details.is_superuser is False:
            user_login(request,user_details)
            return redirect(index)
        else:
            messages.warning(request,"invalid credentials")
            return redirect(login)
    return render(request,'user/page-login.html')

def logout(request):
    user_logout(request)
    return redirect(login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(admin_login)
        return render(request,'user/index.html')
    return redirect(login)

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(admin_login)
        return render(request,'user/shop-list-left.html')
    return redirect(login)