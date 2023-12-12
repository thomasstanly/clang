from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import profileForm, AddressForm, PasswordForm
from product.models import Product_varient
from .models import Address
from order.models import Order,OrderProduct
from admin_side.models import User


# Create your views here.
@login_required
def account(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
        user = request.user
        address = Address.objects.filter(user = user)
        order = Order.objects.filter(user = user,is_ordered = True).order_by('-created_at')
        profile_form = profileForm(instance=user)
        address_form = AddressForm()
        password_form = PasswordForm(user)
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
            'user' : user,
            'addresses' : address,
            'address_form' : address_form,
            'password_form' : password_form,
            'orders': order,
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
        print(id)
        order = Order.objects.get(id=id)
        product = OrderProduct.objects.filter(order=id)
        print(product)
        context = {
            'products': product,
            'order': order,
        }

        return render(request,'user/page-account-order.html',context)

def cancel_order(request,id):
    if request.user.is_authenticated:
        order = Order.objects.get(id=id)  
        
        order_items = OrderProduct.objects.filter(order=order)
        for item in order_items:
            product = Product_varient.objects.get(id=item.product.id)
            product.stock += item.quantity
            product.save()
    
        order.status = 'CANCELLED'
        order.save()
    return redirect('account_app:account')