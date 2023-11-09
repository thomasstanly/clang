from django.urls import path, include
from . import views
app_name = 'customer_app'
urlpatterns = [
    path('',views.customer,name='customer'),
    path('edit/<int:id>',views.customer_edit,name='customer_edit'),
    path('status/<int:id>',views.active_inavtive,name='status')
]