from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('myaccount',views.myaccount, name='userhome'),
    path('owner',views.owner, name='owner'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('ownerout',views.owner_out,name='ownerout'),
    path('usermanager',views.user_manager, name='usermanager'),
    path('blockuser/<int:id>',views.block_user,name='blockuser'),
    path('unblockuser/<int:id>', views.unblock_user, name='unblockuser'),
    path('productmanager',views.product_manager,name='productmanager'),

]
