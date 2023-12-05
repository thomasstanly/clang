from .models import Cart,Wishlist
from django.db.models import Sum,Count

def car_fuc(request):
    count = 0
    try:
        if request.user.is_authenticated:
            cart= Cart.objects.get(user= request.user,complete=False)
            cart_items = cart.cartitems.filter(cart = cart)

            for item in cart_items:
                if item.quantity <= item.product.stock:
                    count += item.quantity
            
        elif 'cart' in request.session:
            for key,value in request.session['cart'].items():
                count += value
    except Cart.DoesNotExist:
        pass

    return {
        'count' : count
    }

def wishlist_func(request):
    count = 0
    try:
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(user = request.user).aggregate(total = Count('user'))
            count = wishlist['total'] or 0
    except Wishlist.DoesNotExist:
        pass
        
    return {
            'wishlist_count': count
    }
           