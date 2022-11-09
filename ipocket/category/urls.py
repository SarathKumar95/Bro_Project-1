from django.urls import path
from category import views

urlpatterns = [
    path('',views.product_manager,name='productmanager'),
    path('editproduct/<int:product_id>',views.product_edit,name='producteditor')
]
