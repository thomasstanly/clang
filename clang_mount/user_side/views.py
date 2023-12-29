from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from admin_side.models import User
from product.models import Product_varient
from cart.models import Cart,CartItems
import random


# signup page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:dashboard')
        return redirect('shop_app:index')
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
            if User.objects.get(username = user):
                messages.warning(request,"username is taken")
                return redirect('user_app:signup')
        except:
                pass
        if ' ' in user:
            messages.warning(request, "Username cannot contain whitespaces")
            return redirect('user_app:signup')

        if ' ' in passw:
            messages.warning(request, "Password cannot contain whitespaces")
            return redirect('user_app:signup')
        
        if not email or '@' not in email:
            messages.info(request,"Email id is not in correct format")
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
            return redirect('admin_app:dashboard')
        return redirect('shop_app:index')
    user = request.session.get('username')
    email = request.session.get('email')
    password = request.session.get('password')
    if request.method == 'POST':
        if str(request.session['otp_key']) == str(request.POST['otp']):
            customer = User.objects.create_user(user_name = user, email = email, password = password )
            customer.save()
            user_login(request,customer)
            return redirect('shop_app:index')
        else:
            messages.error(request,"Invalid OTP")
            return redirect('user_app:otp')   
    return render(request,'user/otp.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
        return redirect('shop_app:index')
    if request.method == "POST":
        email = request.POST["email"]
        passw = request.POST["password"]

        if len(passw) < 8:
                messages.info(request,"invalid credentials")
                return redirect('user_app:user_login')
            
        if not User.objects.filter(email=email):
            messages.error(request, "Invalid Email Adress")
            return redirect('user_app:user_login')
        
        
        customer = User.objects.get(email=email)

        if customer.is_active == True:

            user_details = authenticate(email = email,password = passw)
            
            if user_details is not None and user_details.is_superuser is False:
                user_login(request,user_details)
                guest_cart(request)
                return redirect('shop_app:index')
            else:
                messages.warning(request,"invalid credentials")
                return redirect('user_app:user_login')
        else:
            messages.warning(request,"Sorry your are BLOCKED")
            return redirect('user_app:user_login')
    return render(request,'user/page-login.html')

def guest_cart(request):
    if 'cart' in request.session:
        guest_cart = request.session['cart']
        user = request.user

        cart, created = Cart.objects.get_or_create(user = user)
        if cart.complete == True:
            cart.complete = False
            cart.save()

        for variant_slug,qty in guest_cart.items():
            product_variant = Product_varient.objects.select_related('product_name').get(varient_slug=variant_slug)
            item = CartItems.objects.filter(cart=cart, product=product_variant).first()

            if item:
                item.quantity += qty
                item.save()
            else:
                CartItems.objects.create(cart=cart, product=product_variant, quantity=qty)
        cart.save()
        del request.session['cart']

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def password(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
        return redirect('shop_app:index')
    
    if request.POST.get('action') == 'POST':
        email = request.POST.get('email')
        request.session['email'] = email

        if  User.objects.filter(email = email):
            otp_value = random.randint(100000,999999)
            request.session['otp_key'] = otp_value

            send_mail(
                'OTP verfication from Clang Mount',
                f"{request.session['otp_key']} this is the OTP from Clang Mount to verify your Email. This a computer generated mail",
                'clangmount@gmail.com',
                [email],
                fail_silently=False
            )
            return JsonResponse({'success': True}) 

    return render(request,'user/page-login-password.html')

def Change_pass_otp(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
        return redirect('shop_app:index')
     
    if request.method == 'POST':
        if str(request.session.get('otp_key')) == str(request.POST.get('otp')):
            print(request.POST.get('otp'))
            return redirect('user_app:Change_password')
        else:
            messages.error(request,"Invalid OTP, enter email again")
            del request.session['otp_key']
            return redirect('user_app:password')
    return redirect('user_app:password')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Change_password(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
        return redirect('shop_app:index')
    
    if 'otp_key' not in request.session:
        return redirect('user_app:password')

    if request.method == 'POST':
        del request.session['otp_key']
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')

        if len(password) < 8:
            messages.info(request,"Password minimum 8 characters")
            return redirect('user_app:Change_password')
        
        if password == conf_password:
            email = request.session['email']
            user = User.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            messages.success(request,'Password changed')
            return redirect('user_app:user_login')
        
        else:
            messages.warning(request,"Password doesn't match")
            return redirect('user_app:Change_password')  
        
    return render(request,'user/page-login-new-passowrd.html')

def logout(request):
    user_logout(request)
    return redirect('shop_app:index')
