from django.shortcuts import render,redirect
from product.models import Product,Product_varient
from .models import Cart, CartItems

# Create your views here.
def cart_list(request):
    return render(request,'user/page-cart.html')

def add_to_cart(request,slug):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItems.objects.get_or_create(cart=cart,product=slug)
    
    return redirect('cart_app:cart_list')