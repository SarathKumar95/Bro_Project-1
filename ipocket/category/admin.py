from django.contrib import admin
from .models import * 
# Register your models here.

admin.site.register(Products)
admin.site.register(Categories)
admin.site.register(ProductType)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Wishlist) 

