from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control
from .forms import brand_form,attribute_form, attribute_value_form, product_form, Product_varient_form, product_image
from .models import Brand, attribute, attribute_values, Product, Product_varient


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
def attribute_value(request):
    if request.user.is_authenticated and request.user.is_superuser:
        attr = attribute_values.objects.all()
        print(attr.values())
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

def attribute_value_status(request,id):
    status = attribute_values.objects.get(id=id)
    if request.method == 'POST':
        if status.is_active:
            status.is_active = False
            status.save()
        else:
            status.is_active = True
            status.save()
    return redirect('product_app:attribute_values')

#----------------------------- PRODUCT ----------------------------

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Product.objects.all()
        context = {
            'products' : products
        }
        
        return render(request,'cus_admin/page-products-list.html',context)
    else:
        return redirect('admin_app:admin_login')
    
def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = product_form()
        if request.method == 'POST':
            form = product_form(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Product is added ")
                return redirect('product_app:product')
            else:
                messages.success(request,"Product is not added ")
                return redirect('product_app:add_attribute_value')         
        context = {
            'form' : form
        }
        
        return render(request,'cus_admin/page-form-product.html',context)
    else:
         return redirect('admin_app:admin_login')
    
def product_status(request,slug):
    if request.method == 'POST':
        status = Product.objects.get(product_slug = slug)
        if status.is_active:
            status.is_active = False
            status.save()
        else:
            status.is_active = True
            status.save()
        return redirect('product_app:product')
    
def product_edit(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Product.objects.get(id = id)
        form = product_form(instance=product)
        if request.method == 'POST':
            form = product_form(request.POST,instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "product Updated")
                return redirect('product_app:product')
                
        context = {
            'form' : form,
            'product' :product
        }
        return render(request,'cus_admin/page-product-detail.html',context)
    else:
         return redirect('admin_app:admin_login')
    
def delete_product(request,slug):
    product = Product.objects.get(product_slug = slug)
    product.delete()
    return redirect('product_app:product')
#---------------------- PRODUCT VARIANT ----------------------------------
def variant(request,slug):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Product.objects.get(product_slug = slug)
        variants = Product_varient.objects.filter(product_name=product)
        context = {
            'product' : product,
            'variants' : variants
        }
        return render(request,'cus_admin/page-products-variant.html',context)
    else:
        return redirect('admin_app:admin_login')
    
def variant_add(request,slug):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Product.objects.get(product_slug = slug)
        attributes = attribute.objects.prefetch_related('attribute_values_set').filter(is_active = True)
        form = Product_varient_form(initial={'product_name':product})
        
        attri_data = {}
        for attribut in attributes:
            attribute_value = attribut.attribute_values_set.filter(is_active=True)
            attri_data[attribut.atrribute_name] = attribute_value
        count = attributes.count()

        if request.method == 'POST':
            form = Product_varient_form(request.POST,request.FILES,initial={'product_name':product})
            attri_selected = []
            for attri in range(1,count+1):
                value = request.POST.get('attri_values_'+str(attri))
                if value != 'None':
                    attri_selected.append(int(value))
            print(attri_selected)

            if form.is_valid():
                variant = form.save()
                variant.attribute_name.set(attri_selected)
                variant.save()

                multi_image = request.POST.getlist('multiple_image')

                for image in multi_image:
                    product_image.objects.create(varient_id=variant,image=image)
                return redirect('product_app:variant',slug)

            else:
                context = {
                    'product' : product,
                    'form' : form,
                    'attri_data' : attri_data
                }
                return render(request,'cus_admin/page-products-variant-add.html',context)
        else:
            context = {
                    'product' : product,
                    'form' : form,
                    'attri_data' : attri_data
                }
            return render(request,'cus_admin/page-products-variant-add.html',context)
    else:
        return redirect('admin_app:admin_login')

def variant_edit(request,slug):
    if request.user.is_authenticated and request.user.is_superuser:
        variant = Product_varient.objects.get(varient_slug=slug)
        form = Product_varient_form(instance=variant)
        if request.method == 'POST':
            form = Product_varient_form(request.POST,request.FILES,instance=variant)
            if form.is_valid():
                form.save()
                messages.success(request,"variant updated")
                return redirect('product_app:variant_edit',slug)
        context = {
            'variant' : variant,
            'form' : form
        }
        return render(request,'cus_admin/page-products-variant-edit.html',context)
    else:
        return redirect('product_app:admin_login')
