from django.urls import path,include 
from cart import views


urlpatterns = [
    path('', views.cart_list, name="cart-list" ),
    path('addtocart/<int:product_id>',views.cart_add, name="cart-add"),
]