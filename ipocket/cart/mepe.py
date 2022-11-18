from django.urls import path
from cart import views

urlpatterns = [
    path('add',views.Add_To_Cart, name="AddtoCart")
]
