from django.urls import path
from . import views
app_name = 'order_app'

urlpatterns =[
    path('payment',views.order_payment,name='order_payment'),
    
]