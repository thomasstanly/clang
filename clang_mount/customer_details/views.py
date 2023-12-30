from django.shortcuts import render,redirect
from django.db.models import Q
from admin_side.models import User
from .models import Profile_image
from .forms import ProfileImage
from account.models import Address
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def customer(request):
    if request.user.is_authenticated and request.user.is_superuser:
        customer_detials = User.objects.all().filter(is_superuser = 'False').order_by('-joined_on')

        row = 3
        paginator = Paginator(customer_detials,row)
        page = request.GET.get('page')

        try:
            customer = paginator.page(page)
        except PageNotAnInteger:
            customer = paginator.page(1)
        except EmptyPage:
            customer = paginator.page(paginator.num_pages)


        context = {
            'customer_detials' : customer
        }
        return render(request,'cus_admin/page-customers-list.html',context)
    else:
         return redirect('admin_app:admin_login')
    
def customer_edit(request,id):
    if request.user.is_authenticated and request.user.is_superuser:

        customer = User.objects.get(id=id)
        try:
            image = Profile_image.objects.get(user = customer)
        except Profile_image.DoesNotExist:
            image = False
        
        try:
            address = Address.objects.filter(user = customer).first()
        except:
            address = False

        context = {
            'customer': customer,
            'image': image,
            'address': address,
           
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

def search(request):
    if request.user.is_authenticated and request.user.is_superuser:
        query = request.GET.get('search')
        
        if query == 'active':
            query = True;
        if query == 'inactive':
            query = False;

        if query:
            customer_details = User.objects.filter(Q(username__icontains=query) |
            Q(is_active__icontains=query)).filter(is_superuser = 'False')

            row = 2
            paginator = Paginator(customer_details,row)
            page = request.GET.get('page')

            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            context = {
                'customer_detials' : customer
            }
            return render(request,'cus_admin/page-customers-list.html',context)
        else:
            return redirect('customer_app:customer')
    else:
        return redirect('admin_app:admin_login')