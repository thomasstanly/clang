from django.shortcuts import render,redirect,HttpResponse
from product.models import Product,Product_varient
from .models import Cart, CartItems

# Create your views here.
def cart_list(request):
    cart= Cart.objects.get(user= request.user)
    items = cart.cartitems.all()
    context = {
        'items' : items
    }
    return render(request,'user/page-cart.html',context)

def add_to_cart(request,slug):
    if request.user.is_authenticated:
        product = Product_varient.objects.select_related('product_name').get(varient_slug=slug)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItems.objects.get_or_create(cart=cart,product=product)
        
        return redirect('cart_app:cart_list')
    else:

        return redirect('user_app:user_login')
    
def delete_cart_item(request,id):
    item = CartItems.objects.get(id=id)
    item.delete()
    return redirect('cart_app:cart_list')
    