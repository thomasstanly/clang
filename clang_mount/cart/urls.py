from django.urls import path
from . import views
app_name = 'cart_app'

urlpatterns = [
    path('',views.cart_list,name="cart_list"),
    path('add-to-cart/<slug:slug>',views.add_to_cart,name="add_to_cart"),
]