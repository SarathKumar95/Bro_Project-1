from django.contrib import admin
from .models import * 
# Register your models here.

admin.site.register(Categories)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','generation','series','price','quantity','images')

admin.site.register(Products)
