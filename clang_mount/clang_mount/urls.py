from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin-og/',admin.site.urls),
    path('social_auth/',include('social_django.urls', namespace='social')),
    path('admin/',include('admin_side.urls')),
    path('',include('user_side.urls')),
    path('',include('shop.urls')),
    path('admin/customer/',include('customer_details.urls')),
    path('admin/category/',include('pro_category.urls')),
    path('admin/product/',include('product.urls')),
    path('admin/coupon/',include('coupon.urls')),
    path('admin/sales_report/',include('sales_report.urls')),
    path('admin/banner/',include('banner.urls')),
    path('account/',include('account.urls')),
    path('cart/',include('cart.urls')),
    path('cart/checkout/',include('order.urls')),
    path('wallet/',include('wallet.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
