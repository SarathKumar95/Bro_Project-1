from django.urls import path 
from cart import views

urlpatterns = [
    path('list',views.cart_list,name='cart-list'),
]