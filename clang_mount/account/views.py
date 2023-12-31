from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.cache import cache_control
from .forms import profileForm, AddressForm, PasswordForm
from customer_details.forms import ProfileImage
from customer_details.models import Profile_image
from product.models import Product_varient
from wallet.models import Wallet, Wallet_Transaction
from .models import Address
from order.models import Payment
from order.models import Order,OrderProduct
from datetime import timedelta
from django.utils import timezone
from wallet.models import Wallet,Wallet_Transaction

# Create your views here.

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def account(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
        user = request.user

        try:
            wallet = Wallet.objects.get(user=user)
            wal_tran = Wallet_Transaction.objects.filter(wallet=wallet).order_by('-created_at')
        except:
            wal_tran = None
       
        address = Address.objects.filter(user = user)
        orders = Order.objects.filter(user = user,is_ordered = True).order_by('-created_at')
        for order in orders:
            order.delivery_date = order.payment.created_at + timezone.timedelta(days=3)
            order.total = order.grand_total + order.wallet_amount
            
        profile_form = profileForm(instance=user)
        address_form = AddressForm()
        password_form = PasswordForm(user)

        try:
             image = Profile_image.objects.get(user=user)
        except Profile_image.DoesNotExist:
            image = Profile_image(user=user)
            image.save()

        form = ProfileImage(request.POST or None,request.FILES or None,instance=image)
        if form.is_valid():
            form.save()
            return JsonResponse({'message':'Profile Image Added'})
 
        if request.method == 'POST':
            profile_form = profileForm(request.POST,instance=user)
            
            print(profile_form)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request,'Profile is updated')
                return redirect('account_app:account')
            else:
                messages.error(request,'Profile is not updated')
                return redirect('account_app:account')
        context = {
            'profile_form' : profile_form,
            'image':image,
            'user' : user,
            'addresses' : address,
            'address_form' : address_form,
            'password_form' : password_form,
            'orders': orders,
            'form':form,
            'wallets':wal_tran,
        }
        return render(request,'user/page-account.html',context)
    else:
        return render(request,'user/page-login.html')

def address(request,id):
    user = request.user

    if user.id != id:
        messages.error(request,'You do not have permission to add an address for this user.')
        return redirect('account_app:account')
    
    if request.method == 'POST':
        form = AddressForm(request.POST)
        print(form)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = user
            address.save()
            messages.success(request, 'Address added successfully.')
            return redirect('account_app:account')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    # Append the help text to the error message
                    messages.error(request, f"{error} {form.fields[field].help_text}")
    
        return redirect('account_app:account')
    
def delete_address(request,id):
    if request.user.is_authenticated:
        address = Address.objects.get(id=id)
        address.delete()
    return redirect('account_app:account')

def change_password(request):
    user = request.user
    if request.method == "POST":
        form = PasswordForm(user,request.POST)
        if form.is_valid():
            new = form.save()
            update_session_auth_hash(request,new)
            messages.success(request,'password changed')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    # Append the help text to the error message
                    messages.error(request, f"{error} {form.fields[field].help_text}")

    return redirect('account_app:account')

def order_details(request,id):
    if request.user.is_authenticated:

        order = Order.objects.get(id=id)
        order.total = order.grand_total + order.wallet_amount
        delivery_date = order.payment.created_at.date() + timedelta(days=3)
        return_day = delivery_date + timedelta(days=3)
        current_date = timezone.now().date()
        day = (return_day - current_date).days
       
        product = OrderProduct.objects.filter(order=id)

        context = {
            'products': product,
            'order': order,
            'delivery_date':delivery_date,
            'current_date': current_date,
            'return_day':return_day,
            'day':day,
        }

        return render(request,'user/page-account-order.html',context)

def product_return(request,id):
    if request.user.is_authenticated:
        order_item = OrderProduct.objects.select_related('order').get(id=id)
        order_item.status = 'RETURNED'
        order_item.save()
        product = Product_varient.objects.get(id=order_item.product.id)
        product.stock += order_item.quantity
        product.save()

        try:
            wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=request.user)
        
        wallet.balance += order_item.product_price
        wallet.save()
            
        order = order_item.order
        payment = order.payment
        if payment.amount_paid <= order_item.product_price:
            if order.shipping != None:
                payment.amount_paid = order.shipping
                payment.save()
            else:
                payment.amount_paid = 0
                payment.save()
        else:
            payment.amount_paid -= order_item.product_price
            payment.save()

        wallet_tran = Wallet_Transaction.objects.create(wallet=wallet,type='CREDIT',amount=order_item.product_price)
        wallet_tran.save()

        id = order_item.order.id
        return redirect('account_app:order_details',id)
    
def product_cancel(request,id):
   if request.user.is_authenticated:
        order_item = OrderProduct.objects.select_related('order').get(id=id)
        order_item.status = 'CANCELLED'
        order_item.save()

        product = Product_varient.objects.get(id=order_item.product.id)
        product.stock += order_item.quantity
        product.save()

        if order_item.order.payment.status == 'SUCCESS':
            try:
                wallet = Wallet.objects.get(user=request.user)
            except Wallet.DoesNotExist:
                wallet = Wallet.objects.create(user=request.user)
            
            wallet.balance += order_item.product_price
            wallet.save()

            order = order_item.order
            payment = order.payment

            if payment.amount_paid <= order_item.product_price:
                if order.shipping != None:
                    payment.amount_paid = order.shipping
                    payment.save()
                else:
                    payment.amount_paid = 0
                    payment.save()
            else:
                payment.amount_paid -= order_item.product_price
                payment.save()
            
            wallet_tran = Wallet_Transaction.objects.create(wallet=wallet,type='CREDIT',amount=order_item.product_price)
            wallet_tran.save()

        id = order_item.order.id
        return redirect('account_app:order_details',id)
   else:
       return redirect('home_app:index')
        