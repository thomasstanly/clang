from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.login,name='admin_login'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('product',views.product,name='product'),
    path('add_product',views.add_product,name='add_product'),
    path('product/edit',views.product_edit,name='product_edit'),
    path('brand',views.brands,name='admin_brand'),
    path('categories',views.categories,name='admin_categories'),
    path('order',views.order,name='order'),
    path('order/edit',views.order_edit,name='order_edit'),
    path('customer',views.customer,name='customer'),
    path('customer/edit',views.customer_edit,name='customer_edit'),
    path('logout',views.logout,name='admin_logout')
]
