from django.urls import path
from . import views
app_name = 'sales_app'

urlpatterns = [
    path('',views.sales_report,name='sales_report'),
    path('pdf',views.sales_report_pdf,name='sales_report_pdf'),
    path('excel',views.sales_report_excel,name='sales_report_excel'),
]
