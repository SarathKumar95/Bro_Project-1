from django.urls import path
from cart import views


urlpatterns = [
    path('', views.cart_list, name="cart-list" ),
    path('addtocart/<int:product_id>',views.cart_add, name="cart-add"),
    path('remove/<int:product_id>', views.remove, name="cart-remove"),
    path('ordered', views.Order_Confirm, name="order-success"),

]