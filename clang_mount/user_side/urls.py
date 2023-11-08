from django.urls import path, include
from . import views

urlpatterns = [

    path('signup',views.signup,name='signup'),
    path('login',views.login,name='user_login'),
    path('logout',views.logout, name='user_logout'),
    path('',views.index,name='index'),
    path('home',views.home,name='home'),



]
