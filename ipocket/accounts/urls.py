from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home_page, name='home'),
    path('register', views.register, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('myaccount',views.myaccount, name='userhome'),
    #path('owner',views.owner, name='owner'),
    path('dashboard',views.dashboard, name='dashboard'),
    #path('ownerout',views.owner_out,name='ownerout'),
    path('usermanager',views.user_manager, name='usermanager'),
    path('blockuser/<int:id>',views.block_user,name='blockuser'),
    path('unblockuser/<int:id>', views.unblock_user, name='unblockuser'),
    path('products/',views.products,name="productspage"),
    path('item/<int:product_id>',views.item,name="itempage"),
    path('item/cart/add',views.cart_add,name="cart-add"),
    path('item/cart/list',views.cart_list,name="cart-list"),
    path('item/cart/list/delete',views.cart_delete,name="cart-delete"),
    path('checkout',views.checkout,name='checkout'),
    path('order',views.orderPage,name='order-placed')
]
