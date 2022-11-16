from django.db import models
from category.models import Products
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=255,primary_key=True)
    date_added = models.DateField(auto_now_add=True) 

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField() 


    def __str__(self):
        return self.product 