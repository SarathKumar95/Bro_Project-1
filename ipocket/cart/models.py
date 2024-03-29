from django.db import models
from accounts.models import *
from category.models import *

# Create your models here.

class Cart(models.Model):
    user = models.CharField(max_length=255,null=True,blank=True)
    product_attr = models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product_added')
    variant_color_selected = models.ForeignKey(VariantColor,on_delete=models.CASCADE, related_name='variantColor')
    product_qty = models.IntegerField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255,null=True,blank=True)
    coupon_applied=models.CharField(max_length=100,null=True,blank=True)
    discount_percentage=models.FloatField(null=True,blank=True)
    amount_discounted=models.FloatField(null=True,blank=True)
    grand_total=models.FloatField(null=True,blank=True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.id)

