from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from admin_side.views import login as admin_login
from pro_category.models import Categories
from product.models import Brand,Product_varient,product_image

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
    
        category = Categories.objects.all()
        brand = Brand.objects.all()

        context = {
            'categories' : category,
            'Brands' : brand
        }

        return render(request,'user/index.html',context)
    else:
        category = Categories.objects.all()
        brand = Brand.objects.all()

        context = {
            'categories' : category,
            'Brands' : brand
        }

        return render(request,'user/index.html',context)

##################### SEARCHING PRODUCTS ##################

def search_product(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
        query = request.GET.get('query')

        categories = Categories.objects.all()

        if query:
            products = Product_varient.objects.filter(
                Q(product_name__product_name__icontains=query) |
                Q(product_name__product_brand__Brand_name__icontains=query) |
                Q(product_name__category_id__category_title__icontains=query)
                ).filter(vari_is_active=True)
            if not products.exists():
                return redirect('shop_app:home')
        else:
            return redirect('shop_app:home')
        
        count = products.count()

        context = {
            'products': products,
            'categories':categories,
            'count_product':count,
        }
        return render(request, 'user/shop-list-left.html', context)
    else:
        query = request.GET.get('query')

        categories = Categories.objects.all()

        if query:
            products = Product_varient.objects.filter(
                Q(product_name__product_name__icontains=query) |
                Q(product_name__product_brand__Brand_name__icontains=query) |
                Q(product_name__category_id__category_title__icontains=query)
                ).filter(vari_is_active=True)
            if not products.exists():
                return redirect('shop_app:home')
        else:
            return redirect('shop_app:home')
        
        count = products.count()

        context = {
            'products': products,
            'categories':categories,
            'count_product':count,
        }
        return render(request, 'user/shop-list-left.html', context)

def category_products(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
        products = Product_varient.objects.filter(product_name__category_id__id=id).filter(vari_is_active=True)
        categories = Categories.objects.all()

        context = {
            'products': products,
            'categories':categories,
        }
        return render(request, 'user/shop-list-left.html', context)
    else:
        products = Product_varient.objects.filter(product_name__category_id__id=id).filter(vari_is_active=True)
        categories = Categories.objects.all()

        context = {
            'products': products,
            'categories':categories,
        }

        return render(request, 'user/shop-list-left.html', context)

def brand_products(request, id):
     if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
        products = Product_varient.objects.filter(product_name__product_brand__id=id).filter(vari_is_active=True)
        categories = Categories.objects.all()

        context = {
            'products': products,
            'categories':categories,
        }

        return render(request, 'user/shop-list-left.html', context)
     else:
        products = Product_varient.objects.filter(product_name__product_brand__id=id).filter(vari_is_active=True)
        categories = Categories.objects.all()

        context = {
            'products': products,
            'categories':categories,
        }

        return render(request, 'user/shop-list-left.html', context)

################## HOME ######################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
        products = Product_varient.objects.select_related('product_name').filter(vari_is_active=True)
       
        categories = Categories.objects.all()
        context = {
            'products' : products,
            'categories': categories,
        }
        return render(request,'user/shop-list-left.html',context)
    else:
        products = Product_varient.objects.select_related('product_name').filter(vari_is_active=True)
        categories = Categories.objects.all()
        context = {
            'products' : products,
            'categories': categories
        }
        return render(request,'user/shop-list-left.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def product_details(request,slug):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_login')
        product = Product_varient.objects.select_related('product_name').get(varient_slug=slug)
        variant = Product_varient.objects.get(varient_slug=slug)
        images = product_image.objects.filter(varient_id = variant)
        context = {
            'product' : product,
            'images' : images,
            
        }
        return render(request,'user/shop-product-detail.html',context)
    else:
        product = Product_varient.objects.select_related('product_name').get(varient_slug=slug)
        variant = Product_varient.objects.get(varient_slug=slug)
        images = product_image.objects.filter(varient_id = variant)
        context = {
            'product' : product,
             'images' : images,
        }
        return render(request,'user/shop-product-detail.html',context)
