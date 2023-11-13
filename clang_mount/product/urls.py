from django.urls import path
from . import views
app_name = 'product_app'
urlpatterns = [
    path('',views.product,name='product'),
    path('add_product',views.add_product,name='add_product'),
    path('product/edit',views.product_edit,name='product_edit'),
    path('brand',views.brand,name='brand'),
    path('brand/add',views.add_brand,name='add_brand'),
    path('brand/delete/<int:id>',views.delete_brand,name='delete_brand'),
    path('brand/status/<int:id>',views.brand_status,name='brand_status'),
    path('attribute',views.attribute_list,name='attribute_list'),
    path('attribute/add',views.add_attribute,name='add_attribute'),
    path('attribute/delete/<int:id>',views.delete_attribute,name='delete_attribute'),
    path('attribute/status/<int:id>',views.attribute_status,name='attribute_status'),
    path('attribute/value',views.attribute_values,name='attribute_values'),
    path('attribute/value/add',views.add_attribute_value,name='add_attribute_value'),
    
]