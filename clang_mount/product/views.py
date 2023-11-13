from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control
from .forms import brand_form,attribute_form, attribute_value_form
from .models import Brand, attribute


# --------------------------BRAND----------------------
@cache_control(no_cache=True,must_validate=True,no_store=True)
def brand(request):
    if request.user.is_authenticated and request.user.is_superuser:
        brands = Brand.objects.all()
        add_brand = brand_form()
        context = {
            'brands' : brands,
            'add_brand' : add_brand

        }
        return render(request,'cus_admin/page-brand.html',context)
    else:
         return redirect('admin_app:admin_login')
    
def add_brand(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            add_brand = brand_form(request.POST,request.FILES)
            if add_brand.is_valid():
                add_brand.save()
                print(add_brand)
                messages.success(request,'brand added')
                return redirect('product_app:brand')
            else:
                messages.error(request,"brand exsist")
                redirect('product_app:brand')
        return redirect('product_app:brand')
    else:
        return redirect('admin_app:admin_login')

def delete_brand(request,id):
    brand = Brand.objects.get(id=id)
    brand.delete()
    return redirect('product_app:brand')

def brand_status(request,id):
    brand = Brand.objects.get(id=id)
    if request.method == 'POST':
        if brand.is_active:
            brand.is_active = False
            brand.save()
            print('become false')
        else:
            brand.is_active = True
            brand.save()
            print('become true')
    return redirect('product_app:brand')

#----------------------- ATTRIBUTE---------------------------
def attribute_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        attributes = attribute.objects.all()
        add_attribute = attribute_form()
        context = {
            'attributes' : attributes,
            'add_attribute' : add_attribute
        }
        return render(request, 'cus_admin/page-attribute.html',context)
    else:
        return redirect('admin_app:admin_login')
    
def add_attribute(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            attribute = attribute_form(request.POST)
            if attribute.is_valid():
                attribute.save()
                messages.success(request,"Attribute Created")
                return redirect('product_app:attribute_list')
            else:
                messages.error(request,'Existing Attribute')
                return redirect('product_app:attribute_list')
        else:
            return redirect('product_app:attribute_list')
    else:
        redirect('admin_app:admin_login')

def delete_attribute(request,id):
    attri = attribute.objects.get(id=id)
    attri.delete()
    return redirect('product_app:attribute_list')

def attribute_status(request,id):
    attri = attribute.objects.get(id=id)
    if request.method == 'POST':
        if attri.is_active:
            attri.is_active = False
            attri.save()
            
        else:
            attri.is_active = True
            attri.save()
           
    return redirect('product_app:attribute_list')

#-------------------------ATTRIBUTE VALES ----------------------------
def attribute_values(request,name):
    if request.user.is_authenticated and request.user.is_superuser:
        attr = attribute.objects.get(atrribute_name=name)
        attr_form = attribute_value_form()
        context ={
            'attr' : attr,
            'attr_form' : attr_form
        }
        return render(request,'cus_admin/page-attribute-values.html',context)

def add_attribute_value(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = attribute_value_form(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Value is added ")
                return redirect('product_app:attribute_values')
            else:
                messages.error(request,"Value is existing ")
                return redirect('product_app:attribute_values')
        else:
            return redirect('product_app:attribute_values')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        
        return render(request,'cus_admin/page-products-list.html')
    else:
        return redirect('admin_app:admin_login')
def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        
        return render(request,'cus_admin/page-form-product.html')
    else:
         return redirect('admin_app:admin_login')
def product_edit(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'cus_admin/page-product-detail.html')
    else:
         return redirect('admin_app:admin_login')