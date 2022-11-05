from django.urls import path
from accounts import views

urlpatterns = [
    path('register', views.register, name='signup'),
    path('signin', views.signin, name='signin'),
]
