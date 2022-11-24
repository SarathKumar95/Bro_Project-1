from django.db import models
from accounts.models import *
from category.models import *

# Create your models here.

class Cart(models.Model):
    email = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)