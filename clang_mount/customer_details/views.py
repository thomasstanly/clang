from django.shortcuts import render,redirect
from admin_side.models import User
from .forms import ProfileImage

# Create your views here.
def customer(request):
    if request.user.is_authenticated and request.user.is_superuser:
        customer_detials = User.objects.all().filter(is_superuser = 'False')
        context = {
            'customer_detials' : customer_detials
        }
        return render(request,'cus_admin/page-customers-list.html',context)
    else:
         return redirect('admin_app:admin_login')
def customer_edit(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        customer = User.objects.get(id=id)
        context = {
            'customer': customer
        }
        return render(request,'cus_admin/page-customers-detail.html',context)
    else:
         return redirect('admin_app:admin_login')

def active_inavtive(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        customer = User.objects.get(id=id)
        if customer.is_active:
            customer.is_active = False
        else:
            customer.is_active = True
        customer.save()   
        return redirect('customer_app:customer')
    
# def image(request):
#     if request.method == 'POST':
       
 