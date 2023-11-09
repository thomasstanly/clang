from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.views.decorators.cache import cache_control
from admin_side.views import login as admin_login
from django.contrib import messages
from admin_side.models import User
from admin_side.views import dashboard
import random


# signup page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(dashboard)
        return redirect('user_app:index')
    if request.method == "POST":
        user = request.POST["username"]
        email = request.POST["email"]
        passw = request.POST["password"]
        conpass = request.POST["conf_password"]
        try:
            if User.objects.get(email = email):
                messages.warning(request,"email is taken")
                return redirect('user_app:signup')
        except:
                pass
        try:
            if User.objects.get(user_name = user):
                messages.warning(request,"username is taken")
                return redirect('user_app:signup')
        except:
                pass
        if not email or '@' not in email:
            messages.info(request,"Email id is not correct")
            return redirect('user_app:signup')
        if passw != conpass:
            messages.warning(request,"Password is incorrect")
            return redirect('user_app:signup')
        if len(passw) < 8:
            messages.info(request,"Password minimum 8 characters")
            return redirect('user_app:signup')
        request.session['username'] = user
        request.session['password'] = passw
        request.session['email'] = email
        return redirect('user_app:otp_verification')
    return render(request,'user/page-login-register.html')

# otp sending take place
def otp_verification(request):
    otp_value = random.randint(100000,999999)
    request.session['otp_key'] = otp_value

    send_mail(
        'OTP verfication from Clang Mount',
        f"{request.session['otp_key']} this is the OTP from Clang Mount to verify your Email. This a computer generated mail",
        'clangmount@gmail.com',
        [request.session['email']],
        fail_silently=False
    )
    return redirect('user_app:otp')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def otp(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(dashboard)
        return redirect('user_app:index')
    user = request.session.get('username')
    email = request.session.get('email')
    password = request.session.get('password')
    if request.method == 'POST':
        if str(request.session['otp_key']) == str(request.POST['otp']):
            customer = User.objects.create_user(user_name = user, email = email, password = password )
            customer.save()
            user_login(request,customer)
            return redirect('user_app:index')        
    return render(request,'user/otp.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(admin_login)
        return redirect('user_app:index')
    if request.method == "POST":
        email = request.POST["email"]
        passw = request.POST["password"]
        user_details = authenticate(email = email,password = passw)
        if user_details is not None and user_details.is_superuser is False:
            user_login(request,user_details)
            return redirect('user_app:index')
        else:
            messages.warning(request,"invalid credentials")
            return redirect('user_app:user_login')
    return render(request,'user/page-login.html')

def logout(request):
    user_logout(request)
    return redirect('user_app:index')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(admin_login)
        return render(request,'user/index.html')
    return render(request,'user/index.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(admin_login)
        return render(request,'user/shop-list-left.html')
    return render(request,'user/index.html')