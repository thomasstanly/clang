from django.urls import path, include
from . import views

urlpatterns = [
    path('admin',views.login,name='admin_login'),
    path('admin/dashboard',views.dashboard,name='dashborad'),
    path('admin/product',views.product,name='product'),
    path('admin/add_product',views.add_product,name='add_product'),
    path('admin/product/edit',views.product_edit,name='product_edit'),
    path('admin/brand',views.brands,name='admin_brand'),
    path('admin/categories',views.categories,name='admin_categories'),
    path('admin/order',views.order,name='order'),
    path('admin/order/edit',views.order_edit,name='order_edit'),
    path('admin/customer',views.customer,name='customer'),
    path('admin/customer/edit',views.customer_edit,name='customer_edit'),
    path('admin/logout',views.logout,name='admin_logout')
]
