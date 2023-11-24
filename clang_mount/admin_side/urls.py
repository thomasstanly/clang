from django.urls import path, include
from . import views
app_name = 'admin_app'
urlpatterns = [
    path('',views.login,name='admin_login'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('order',views.order,name='order'),
    path('order/edit',views.order_edit,name='order_edit'),
    path('logout',views.logout,name='admin_logout')
]
