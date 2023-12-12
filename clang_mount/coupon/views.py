from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Coupon
from .forms import CouponForm

# Create your views here.
def coupon(request):
    if request.user.is_authenticated:
        coupons = Coupon.objects.all().order_by('-created_at')
        if request.method == 'POST':
            form = CouponForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Coupon Added Successfully')
                return redirect('coupon_app:coupon')
        else:
            form = CouponForm()

        context = {
            'form_coupon': form,
            'coupons':coupons,
        }
        return render(request,'cus_admin/coupon.html',context)
    
def status(request,id):
    if request.method == 'POST':
        status = Coupon.objects.get(id =id)
        if status.is_active:
            status.is_active = False
            status.save()
        else:
            status.is_active = True
            status.save()
        return redirect('coupon_app:coupon')

def delete(request,id):
    product = Coupon.objects.get(id = id)
    product.delete()
    return redirect('coupon_app:delete')

def edit(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        coupon = Coupon.objects.get(id = id)
        coupons = Coupon.objects.all().order_by('-created_at')
        form = CouponForm(instance=coupon)
        if request.method == 'POST':
            form = CouponForm(request.POST,instance=coupon)
            if form.is_valid():
                form.save()
                messages.success(request, "Coupon Updated")
                return redirect('coupon_app:coupon')
                
        context = {
            'form_coupon' : form,
            'coupon' :coupon,
            'coupons':coupons,
        }
        return render(request,'cus_admin/coupon.html',context)
    else:
         return redirect('admin_app:admin_login')
