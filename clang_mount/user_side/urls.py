from django.urls import path, include
from . import views
app_name = 'user_app'
urlpatterns = [
    path('signup',views.signup,name='signup'),
    path('otp',views.otp,name='otp'),
    path('login',views.login,name='user_login'),
    path('logout',views.logout, name='user_logout'),
    path('otp_verification',views.otp_verification,name="otp_verification"),
    path('',views.index,name='index'),
    path('home',views.home,name='home'),
    path('<slug:slug>',views.product_details,name='product_details')
]
