from django.urls import path
from .views import Banner
app_name = 'banner_app'

urlpatterns =[
    path('',Banner.as_view(),name="banner"),
]