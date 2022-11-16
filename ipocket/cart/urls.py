from django.urls import path,include 
from cart import views


urlpatterns = [
    path('', views.cart_list, name="cart-list" ),
]