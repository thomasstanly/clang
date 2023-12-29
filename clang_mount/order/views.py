from django.shortcuts import render, redirect
from django.urls import reverse
from django .db.models import Q
from django.contrib import messages
from account.models import Address
from cart.models import Cart,CartItems
from wallet.models import Wallet, Wallet_Transaction
from .models import Payment,Order,OrderProduct
from product.models import Product_varient
from coupon.models import Coupon
import uuid
import razorpay
from datetime import timedelta
from django.conf import settings
from io import BytesIO
from django.views import View
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os


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
                wallet_checked = int(request.POST.get('add_wallet'))
            except:
                wallet_checked = 0

            try:
                try:
                    coupon = request.session['coupon']
                except KeyError:
                    coupon = None
                coupon_taken = Coupon.objects.get(coupon_code=coupon)
                del request.session['coupon']
            except Coupon.DoesNotExist:
                coupon_taken = None

            try:
                delivery_address = Address.objects.get(id=address)
            except Address.DoesNotExist:
                messages.error(request,"Sorry address didn't find")
                return redirect('cart_app:checkout')
            
            request.session['payment'] = payment_method
   
            if 'order_id' not in request.session:
                random = int(uuid.uuid4().hex[:8],16)
                order_id = f"#{random}"
                request.session['order_id'] = order_id
                
            try:
                order_details = Order.objects.get(user=request.user, order_no=request.session['order_id'])
            except Order.DoesNotExist:
                order_details = Order(
                user=request.user,
                order_no=request.session['order_id'],
                delivery_address=delivery_address,
                grand_total=total,
                sub_total=sub_total,
                shipping=shipping,
                coupon=coupon_taken
            )
                order_details.save()

            # Now you can update the order_details object as needed
            order_details.delivery_address = delivery_address
            order_details.grand_total = total
            order_details.sub_total = sub_total
            order_details.shipping = shipping
            order_details.save()

            if coupon_taken is not None :
                order = Order.objects.get(order_no = request.session['order_id'])
                order.coupon = coupon_taken
                order.grand_total = total
                order.save()

            grand_total = order_details.grand_total
            wallet_balance = 0
            try:
                wallet = Wallet.objects.get(user=request.user,is_active=True)
            except Wallet.DoesNotExist:
                wallet = Wallet.objects.create(user=request.user)
                wallet.save()
            print(wallet.balance)
            if wallet_checked == 1:
                if wallet.balance <= float(grand_total):
                    grand_total = float(grand_total) - wallet.balance
                    order_details.grand_total = grand_total
                    order_details.wallet_amount = wallet.balance
                    order_details.save()
                else:
                    order_details.wallet_amount = float(grand_total)
                    order_details.grand_total = 0
                    order_details.save()

            print(order_details.grand_total)
            print(order_details.wallet_amount)
            print(wallet.balance)

            return redirect('order_app:online_payment')
        else:
            return redirect('cart_app:checkout')
    return redirect('user_app:user_login')


def online_payment_and_cod(request):

    if request.user.is_authenticated:
        order_id = request.session['order_id']
        payment_method = request.session['payment']
        print(payment_method)
        order_details = Order.objects.get(order_no=order_id)
        cart = Cart.objects.get(user=request.user,complete=False)
        items = CartItems.objects.filter(cart=cart)
        for item in items:
            item.total_price = item.sub_total() - item.discount()

        if payment_method == 'ONLINE_PAYMENT':
            try:
                client = razorpay.Client(auth=(settings.KEY, settings.SECRET_KEY))
                payment = client.order.create({ "amount": int(order_details.grand_total) * 100, "currency": "INR"})
            except:
                payment = False
        else:
            payment = False

        success_page_url = request.build_absolute_uri(reverse('order_app:success'))
        failed_page_url = request.build_absolute_uri(reverse('order_app:failed'))
        
        context = {
            'order':order_details,
            'items':items,
            'payment_method':payment_method,
            'payment':payment,
            'success': success_page_url,
            'failed_': failed_page_url,

        }
        return render(request,'user/shop-summary.html',context)
    else:
        return redirect('user_app:user_login')

def payment_success(request):
   
    payment_id = request.GET.get('payment_id')
    payment_order_id = request.GET.get('payment_order_id')
    order_id = request.session['order_id']
    payment_sign = request.GET.get('payment_sign')
    payment_method = request.session['payment']


    try:
         order = Order.objects.get(user=request.user,is_ordered=False,order_no=order_id)
         grand_total = order.wallet_amount + order.grand_total
    except Exception:
        messages.error(request,'order not found')
        return redirect('shop_app:index')
    
    if payment_method == 'ONLINE_PAYMENT':
        payment_details = Payment.objects.create(user=request.user,payment_id=payment_id,
        payment_order_id=payment_order_id,payment_signature=payment_sign,amount_paid=grand_total,status='SUCCESS',payment_method=payment_method)
        payment_details.save()

        wallet = Wallet.objects.get(user=request.user,is_active=True)
        wallet.balance = wallet.balance - order.wallet_amount
        wallet.save()

        wallet_tran = Wallet_Transaction.objects.create(wallet=wallet,type='DEBIT',amount=order.wallet_amount)
        wallet_tran.save()

        cart = Cart.objects.get(user=request.user)
        items = CartItems.objects.filter(cart=cart)

        for item in items:
            price = item.sub_total() - item.discount()
            order_product = OrderProduct.objects.create(order=order,user=request.user,product=item.product,
            quantity=item.quantity,product_price=price,is_ordered=True,)
            order_product.save()

            product = Product_varient.objects.get(id=item.product.id)
            product.stock -= item.quantity
            product.save()
            item.delete()
        
        order.payment = payment_details
        order.is_ordered = True
        order.save()

        

        del request.session['address_id']
        del request.session['order_id']
        del request.session['payment']
        messages.success(request,'Order placed and payment successfull')
        return redirect('shop_app:index')

    if payment_method == 'COD':
        payment_details = Payment.objects.create(user=request.user,payment_id=payment_id,
        payment_order_id=payment_order_id,payment_signature=payment_sign,amount_paid=order.grand_total,status='PENDING',payment_method=payment_method)
        payment_details.save()

        wallet = Wallet.objects.get(user=request.user,is_active=True)
        wallet.balance = wallet.balance - order.wallet_amount
        wallet.save()

        wallet_tran = Wallet_Transaction.objects.create(wallet=wallet,type='DEBIT',amount=order.wallet_amount)
        wallet_tran.save()

        cart = Cart.objects.get(user=request.user)
        items = CartItems.objects.filter(cart=cart)

        for item in items:
            price = item.sub_total() - item.discount()
            order_product = OrderProduct.objects.create(order=order,user=request.user,product=item.product,
            quantity=item.quantity,product_price=price,is_ordered=True,)
            order_product.save()

            product = Product_varient.objects.get(id=item.product.id)
            product.stock -= item.quantity
            product.save()
            item.delete()
        
        order.payment = payment_details
        order.is_ordered = True
        order.save()

        del request.session['address_id']
        del request.session['order_id']
        del request.session['payment']
        messages.success(request,'Order placed ')
        return redirect('shop_app:index')
    
def payment_failed(request):
    context = {
    'method': request.GET.get('method'),
    'error_code': request.GET.get('error_code'),
    'error_description': request.GET.get('error_description'),
    'error_reason': request.GET.get('error_reason'),
    'error_payment_id': request.GET.get('error_payment_id'),
    'error_order_id': request.GET.get('error_order_id')
    }
    messages.success(request,'payment failed')
    return redirect('shop_app:index')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class GenerateInvoice(View):
    
    def get(self, request, id, *args, **kwargs):
        try:
            order = Order.objects.get(id = id, user = request.user)
            delivery_date = order.created_at + timedelta(days=3)
        except:
            return HttpResponse("505 Not Found")
            
        data = {
            'order_id': order.order_no,
            'transaction_id': order.payment.payment_id,
            'user_email': order.user.email,
            'date': order.created_at,
            'first_name': order.user.first_name,
            'last_name': order.user.last_name,
            'grand_total': order.grand_total + order.wallet_amount,
            'order_items': OrderProduct.objects.filter(order=order),
            'delivery_date':delivery_date,
            'shipping': order.shipping,
            'sub_total': order.sub_total,
        }
        pdf = render_to_pdf('user/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
