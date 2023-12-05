from django.urls import path, include
from . import views
app_name = 'user_app'
urlpatterns = [
    path('signup',views.signup,name='signup'),
    path('otp',views.otp,name='otp'),
    path('login',views.login,name='user_login'),
    path('login/forgot-password',views.password,name='password'),
    path('login/pass-otp',views.Change_pass_otp,name='Change_pass_otp'),
    path('login/change-password',views.Change_password,name='Change_password'),
    path('logout',views.logout, name='user_logout'),
    path('otp_verification',views.otp_verification,name="otp_verification"),
    
]
