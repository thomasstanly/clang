from django.shortcuts import render,redirect
from django .db.models import Q
from django.contrib import messages
from account.models import Address
from cart.models import Cart,CartItems
from .models import Payment,Order,OrderProduct
from product.models import Product_varient
import uuid

# Create your views here.


def order_payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            if 'address_id' not in  request.session:
                messages.error(request,'Please select a address')
                return redirect('cart_app:checkout')
            
            payment_method = request.POST.get('payment')
            sub_total = request.POST.get('sub_total')
            shipping = request.POST.get('shipping')
            total = request.POST.get('grand_total')
            address = request.session['address_id']

            try:
                delivery_address = Address.objects.get(id=address)
            except Address.DoesNotExist:
                messages.error(request,"Sorry address didn't find")
                return redirect('cart_app:checkout')
                

            order_id = int(uuid.uuid4().hex[:8],16)
            order_id = f"#{order_id}"
            
            if payment_method == "COD":
                payment_details = Payment.objects.create(user=request.user, payment_order_id=order_id,amount_paid=total,
                                                    status='PENDING',payment_method=payment_method)
                payment_details.save()
                
                order_details = Order.objects.create(user=request.user,payment=payment_details,order_no=order_id,
                                                    delivery_address=delivery_address,grand_total=total,sub_total=sub_total,shipping=shipping)
                order_details.save()
                
            elif payment_method == 'ONLINE_PAYMENT':
                messages.info(request,"For now Cash on delivery is only available")
                return redirect('cart_app:checkout')
            
            cart = Cart.objects.get(user=request.user,complete=False)
            items = CartItems.objects.filter(cart=cart)
            for item in items:
                price = item.sub_total() - item.discount()
                ordered_prduct = OrderProduct.objects.create(user=request.user,order=order_details, product=item.product,
                                                              quantity=item.quantity,product_price=price)
                product = Product_varient.objects.get(id=item.product.id)
                product.stock -= item.quantity
                product.save()

            cart.complete = True
            cart.save()
            items.delete()
            del request.session['address_id']
            messages.success(request,'Order Placed')
            return redirect('shop_app:index')

            
        return redirect('cart_app:checkout')
    return redirect('user_app:user_login')