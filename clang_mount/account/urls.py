from django.urls import path
from . import views
app_name = 'account_app'

urlpatterns = [
    path('',views.account,name='account'),
    path('address/<int:id>',views.address,name='address'),
    path('address/delete/<int:id>',views.delete_address,name='delete_address'),
    path('change_password',views.change_password,name='change_password'),
    path('<int:id>',views.order_details,name= 'order_details'),
    path('cancel/<int:id>',views.cancel_order,name= 'cancel_order')
]
