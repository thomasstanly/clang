from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import profileForm, AddressForm, PasswordForm
from .models import Address
from admin_side.models import User


# Create your views here.
@login_required
def account(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
        user = request.user
        address = Address.objects.filter(user = user)
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
            messages.error(request, 'Please check the form.')
    
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