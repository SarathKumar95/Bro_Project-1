from django.db import models
from accounts.models import *
from category.models import *

# Create your models here.

class Cart(models.Model):
    user = models.CharField(max_length=255,null=True,blank=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    #session_id = models.CharField(max_length=25,null=True,blank=True)

    def __str__(self):
        return self.product.product_name

