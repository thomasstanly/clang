from django.urls import path
from . import views
app_name = 'order_app'

urlpatterns =[
    path('payment',views.order_payment,name='order_payment'),
    path('payment/online-pyment',views.online_payment_and_cod,name='online_payment'),

    path('payment/success',views.payment_success,name='success'),
    path('payment/failed',views.payment_failed,name='failed'),
    
]