from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home_page, name='home'),
    path('register', views.register, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('myaccount',views.myaccount, name='userhome'),
    path('myorder',views.myorder, name='my-order'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('usermanager',views.user_manager, name='usermanager'),
    path('blockuser/<int:id>',views.block_user,name='blockuser'),
    path('unblockuser/<int:id>', views.unblock_user, name='unblockuser'),
    path('products/',views.products,name="productspage"),
    path('item/<int:product_id>',views.item,name="itempage"),
    path('item/cart/add',views.cart_add,name="cart-add"),
    path('item/cart/list',views.cart_list,name="cart-list"),
    path('item/cart/list/delete',views.cart_delete,name="cart-delete"),
    path('item/cart/list/update',views.cart_update,name="cart-update"),
    path('checkout',views.checkout,name='checkout'),
    #path('complete',views.payment_complete,name='complete'),
    #path('order/<str:t_no>',views.orderPage,name='order-placed'),
    path('ordermanager',views.order_manager, name='order-list'),
    path('ordermanager/edit/<int:id>',views.order_edit, name='order-edit'),
    path('ordermanager/info/<int:id>',views.order_info, name='order-info'),
    path('ordermanager/delete/<int:id>',views.order_delete, name='order-delete'),
    path('orderitem/edit/<int:id>',views.orderitem_edit, name='orderitem-edit'),
    path('orderitem/info/delete/<int:id>',views.orderitem_delete, name='orderitem-delete'),
    path('orderitem/info/cancel/<int:id>',views.orderitem_cancel, name='orderitem-cancel'),
    path('orderpage/<str:tracking_no>',views.OrderPage, name='order-page'),
    #path('guest',views.guest,name='guest')     
    path('ordereditem/<int:id>',views.ordered, name='ordered-items'),
]
