from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin-og/',admin.site.urls),
    path('admin/',include('admin_side.urls')),
    path('',include('user_side.urls')),
    path('',include('shop.urls')),
    path('admin/customer/',include('customer_details.urls')),
    path('admin/category/',include('pro_category.urls')),
    path('admin/product/',include('product.urls')),
    path('account/',include('account.urls')),
    path('cart/',include('cart.urls')),
    path('cart/ceckout/',include('order.urls'))
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
