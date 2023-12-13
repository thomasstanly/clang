from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.cache import cache_control
from django.db.models import Sum
from django.contrib import messages
from django.http import JsonResponse
from product.models import Product_varient
from account.forms import AddressForm
from .models import Cart, CartItems, Wishlist
from order.models import Order
from coupon.models import Coupon
from account.models import Address
from django.db.models import Q,Count
import uuid

# Create your views here.   
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def cart_list(request):
    if request.user.is_authenticated:
        try:
            cart= Cart.objects.get(user= request.user,complete=False)
        except Cart.DoesNotExist:
            return render(request,'user/page-cart.html')

        items = cart.cartitems.all()
        for item in items:
            if item.product.stock <= 0:
                item.delete()
                
        sub_total = sum(item.sub_total() for item in items)
        dis_total = sum(item.discount() for item in items)
        total = sub_total - dis_total
        context = {
            'items' : items,
            'sub_total': sub_total,
            'dis_total': dis_total,
            'total': total,
        }
        return render(request,'user/page-cart.html',context)
    elif 'cart' in request.session:

        cart_dict = request.session.get('cart', {})
        variant_slug = list(cart_dict.keys())
        products = Product_varient.objects.select_related('product_name').filter(varient_slug__in=variant_slug)
        sub_total = sum(product.price * cart_dict[product.varient_slug] for product in products)
        dis_total = sum((product.price*product.discount_percentage)/100 * cart_dict[product.varient_slug]  for product in products)
        total = sub_total-dis_total
        context = {
            'items' : [{'product': product, 'quantity':cart_dict[product.varient_slug]} for product in products],
            'sub_total': sub_total,
            'dis_total': dis_total,
            'total': total,
        }
        return render(request,'user/page-cart.html',context)
    else:
         return render(request,'user/page-cart.html')

def add_to_cart(request,slug):
    if request.user.is_authenticated:
        product = Product_varient.objects.select_related('product_name').get(varient_slug=slug)
        cart, created = Cart.objects.get_or_create(user=request.user)

        if product.stock <= 0:
            messages.warning(request,'out of stock!')
            return redirect('shop_app:product_details',slug)
        
        if cart.complete == True:
            cart.complete = False
            cart.save()
        cart_item, created = CartItems.objects.get_or_create(cart=cart,product=product)

        try:
            wishlist = Wishlist.objects.get(Q(user=request.user) & Q(product= product))
            wishlist.delete()
        except:
            pass
            
        return redirect('cart_app:cart_list')
    else:
        if 'cart' not in request.session:
            request.session['cart'] = {}
        cart_dict = request.session['cart']
        if slug in cart_dict:
            cart_dict[slug] += 1
        else:
            cart_dict[slug] = 1
        request.session.modified = True
        messages.info(request, f"Product added to the guest cart")
        return redirect('cart_app:cart_list')

def update_cart(request):

    if request.user.is_authenticated:
        if request.POST.get('action') == 'POST':
            item_id = int(request.POST.get('item_id'))
            item_qty = int(request.POST.get('item_qty'))
            
            item = CartItems.objects.get(id=item_id)

            if item_qty > item.product.stock:
                return JsonResponse({'success': False, 'error': 'out of stock'})
            item.quantity = item_qty
            item.save()
            cart = Cart.objects.get(user = request.user)
            return JsonResponse({'success': True, 'message':'added'})
        
    elif 'cart' in request.session:     
        if request.POST.get('action') == 'POST':
            product_id = int(request.POST.get('item_id'))
            quantity = int(request.POST.get('item_qty'))
            product = Product_varient.objects.select_related('product_name').get(id = product_id)

            if quantity >= product.stock:
                return JsonResponse({'success': False, 'error': 'out of stock'})

            variant_slug = product.varient_slug
            request.session['cart'][variant_slug] = quantity
            request.session.save()
            return JsonResponse({'success': True, 'message':'added'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
    
def delete_cart_item(request,id):
    if request.user.is_authenticated:
        item = CartItems.objects.get(id=id)
        item.delete()
        cart = Cart.objects.get(user=request.user)
        cart.coupon = None
        cart.save()

        return redirect('cart_app:cart_list')
    else:
        if 'cart' in request.session:
            item = Product_varient.objects.select_related('product_name').get(id=id)
            variant_slug = item.varient_slug
            del request.session['cart'][variant_slug]
            request.session.save()
            return redirect('cart_app:cart_list')

# views for wishlist page
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def wishlist(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user = request.user)
        context = {
            'wishlists': wishlist
        }
        return render(request,'user/page-wishlist.html',context)
    return render(request,'user/page-wishlist.html')

def add_wishlist(request):
    if request.user.is_authenticated:
        if request.POST.get('action') == 'POST':
            slug = request.POST.get('slug')
            product = Product_varient.objects.select_related('product_name').get(varient_slug=slug)

            try:
                cart_item = CartItems.objects.get(cart__user=request.user, product=product)
                return JsonResponse({'success': False, 'error': 'Product is already in the cart.'})
            except CartItems.DoesNotExist:
                pass
            
            try:
                wishlist = Wishlist.objects.get(Q(user= request.user) & Q(product=product))
                return JsonResponse({'success': False, 'error': 'Product is already in the whislist.'})
            except Wishlist.DoesNotExist:
                pass
            
            wishlist = Wishlist.objects.create(user=request.user, product= product)
            wishlist.save()
            wishlist = Wishlist.objects.filter(user = request.user).count()
            return JsonResponse({'success': True, 'wishlist_count':wishlist})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def delete_wishlist(request,slug):
    if request.user.is_authenticated:
            product = Product_varient.objects.select_related('product_name').get(varient_slug=slug)
            wishlist = Wishlist.objects.get(Q(user=request.user) & Q(product= product))
            wishlist.delete()
            return redirect('cart_app:wishlist')
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# views for checkout page

def checkout(request):
    if request.user.is_authenticated:

        if request.POST.get('action') == 'POST':
            request.session['address_id'] = request.POST.get('address')
            print(request.session['address_id'])
            return JsonResponse({'success': True})
 
        cart = Cart.objects.get(user = request.user,complete=False)
        
        coupons = Coupon.objects.filter(is_active=True).order_by('-created_at')
        count = CartItems.objects.filter(cart = cart).count()
        if count == 0:
            return redirect('cart_app:cart_list')
        
        items = CartItems.objects.filter(cart = cart)
        for item in items:
            if item.quantity > item.product.stock:
                messages.warning(request,"out of Stock")
                return redirect('cart_app:cart_list')
            
        sub_total = sum(item.sub_total() for item in items)
        dis_total = sum(item.discount() for item in items)

        shipping = 0
        if sub_total < 30000:
            shipping = (sub_total * 20)/1000

        sub_total = sub_total - dis_total
        total = shipping + sub_total
        
        
        try:
            select_coupon = Coupon.objects.get(coupon_code =request.session['coupon'])
            value = (total * select_coupon.dis_percentage)/100
            total = round(total - value,2)
            
        except:
            pass
        
        addresses = Address.objects.filter(user = request.user).order_by('-created_at')
        address_form = AddressForm()
        
        context = {
            'items':items,
            'sub_total': sub_total,
            'shipping': shipping,
            'addresses':addresses,
            'total': total,
            'addresses':addresses,
            'user': request.user,
            'address_form':address_form,
            'coupons':coupons,
            'coupon_value':request.session.get('coupon', None),
        }
        
    return render(request,'user/shop-checkout.html',context)

def coupon_verfication(request):
    if request.method == "POST":
            coupon_value = request.POST['coupon-code']
            print(coupon_value)

            try: 
                coupon = Coupon.objects.get(coupon_code = coupon_value)
                request.session['coupon'] = coupon.coupon_code
            except Coupon.DoesNotExist:
                return redirect('cart_app:checkout')
            
            cart = Cart.objects.get(user=request.user)
            items = CartItems.objects.filter(cart = cart)
            sub_total = sum(item.sub_total() for item in items)
            dis_total = sum(item.discount() for item in items)

            shipping = 0
            if sub_total < 30000:
                shipping = (sub_total * 20)/1000

            sub_total = sub_total - dis_total
            total = shipping + sub_total
            
            if total < coupon.min_amount:
                messages.warning(request,'The coupon has minimum value!')
                return redirect('cart_app:checkout')
            messages.success(request,'Coupon added successfully')
            return redirect('cart_app:checkout')

def address(request,id):
    user = request.user

    if user.id != id:
        messages.error(request,'You do not have permission to add an address for this user.')
        return redirect('account_app:account')
    
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = user
            address.save()
            messages.success(request, 'Address added successfully.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} {form.fields[field].help_text}")
    
        return redirect('cart_app:checkout')
    

