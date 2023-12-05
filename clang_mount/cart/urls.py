from django.urls import path
from . import views
app_name = 'cart_app'

urlpatterns = [
    path('',views.cart_list,name="cart_list"),
    path('add-to-cart/<slug:slug>',views.add_to_cart,name="add_to_cart"),
    path('delete/<int:id>',views.delete_cart_item,name="delete_cart_item"),
    path('update-cart',views.update_cart,name="update_cart"),
    
    path('wishlist',views.wishlist,name='wishlist'),
    path('wishlist-add',views.add_wishlist,name='add_wishlist'),
    path('wishlist-delete/<slug:slug>',views.delete_wishlist,name='delete_wishlist'),

    path('checkout',views.checkout,name='checkout'),
    path('address/<int:id>',views.address,name='address'),
]