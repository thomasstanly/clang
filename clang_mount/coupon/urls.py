
from django.urls import path
from . import views
app_name = 'coupon_app'

urlpatterns = [
    path('',views.coupon,name='coupon'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('status/<int:id>',views.status,name='status'),
    path('delete/<int:id>',views.delete,name='delete'),

]
