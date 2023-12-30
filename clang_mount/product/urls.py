from django.urls import path
from . import views
app_name = 'product_app'
urlpatterns = [
    # product
    path('',views.product,name='product'),
    path('add_product',views.add_product,name='add_product'),
    path('status/<slug:slug>',views.product_status,name='product_status'),
    path('delete/<slug:slug>',views.delete_product,name='delete_product'),
    path('edit/<int:id>',views.product_edit,name='product_edit'),
    path('search',views.search,name='search'),

    # product variant
    path('variant/<slug:slug>',views.variant,name='variant'),
    path('variant/add/<slug:slug>',views.variant_add,name='variant_add'),
    path('variant/status/<slug:slug>/<slug:p_slug>',views.variant_status,name='variant_status'),
    path('variant/edit/<slug:slug>/<slug:p_slug>',views.variant_edit,name='variant_edit'),
    path('variant/delete/<slug:slug>/<slug:p_slug>',views.delete_variant,name='delete_variant'),
    path('variant/delete/image/<int:id>/<slug:slug>/<slug:p_slug>',views.image_variant,name='image_variant'),

    #brand
    path('brand',views.brand,name='brand'),
    path('brand/add',views.add_brand,name='add_brand'),
    path('brand/delete/<int:id>',views.delete_brand,name='delete_brand'),
    path('brand/status/<int:id>',views.brand_status,name='brand_status'),

    #attribute
    path('attribute',views.attribute_list,name='attribute_list'),
    path('attribute/add',views.add_attribute,name='add_attribute'),
    path('attribute/delete/<int:id>',views.delete_attribute,name='delete_attribute'),
    path('attribute/status/<int:id>',views.attribute_status,name='attribute_status'),
    
    #attribute
    path('attribute/value',views.attribute_value,name='attribute_values'),
    path('attribute/value/add',views.add_attribute_value,name='add_attribute_value'),
    path('attribute/value/status/<int:id>',views.attribute_value_status,name='attribute_value_status'),
    
]