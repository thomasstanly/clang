from django.urls import path
from . import views
app_name = 'account_app'

urlpatterns = [
    path('',views.account,name='account'),
    path('address/<int:id>',views.address,name='address'),
    path('change_password',views.change_password,name='change_password'),
]
