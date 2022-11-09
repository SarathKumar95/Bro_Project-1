from django.urls import path
from category import views

urlpatterns = [
    path('',views.product_manager,name='productmanager'),
]
