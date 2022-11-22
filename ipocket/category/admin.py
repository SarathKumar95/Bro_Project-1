from django.contrib import admin
from .models import * 
from image_cropping import ImageCroppingMixin
# Register your models here.

admin.site.register(Products)
admin.site.register(Categories)
admin.site.register(ProductType)


