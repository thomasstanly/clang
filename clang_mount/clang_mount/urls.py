from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin-og/',admin.site.urls),
    path('admin/',include('admin_side.urls')),
    path('',include('user_side.urls')),
    path('admin/customer/',include('customer_details.urls')),
]
