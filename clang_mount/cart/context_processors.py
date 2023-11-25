from .models import Cart
from django.db.models import Count,Sum

def car_fuc(request):
    if request.user.is_authenticated:
        cart= Cart.objects.get(user= request.user)
        cart_items = cart.cartitems.filter(cart = cart).aggregate(total=Count('cart'))
        count = cart_items['total'] or 0
    return {
        'count' : count
    }