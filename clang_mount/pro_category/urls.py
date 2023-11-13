from django.urls import path, include
from . import views
app_name = 'category_app'

urlpatterns = [
   path('',views.categories,name='admin_categories'),
   path('add_category',views.add_categories,name='add_categories'),
   path('edit_category/<int:id>',views.edit_categories,name='edit_categories'),
   path('delete_category/<int:id>',views.delete_categories,name='delete_categories'),
]