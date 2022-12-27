from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=50, unique=True)
    mobile_number = PhoneNumberField(unique=True, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class BillingAddress(models.Model):
     user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
     addressline=models.TextField(max_length=500,null=True,blank=True)
     state=models.CharField(max_length=100,null=True,blank=True) 
     city=models.CharField(max_length=100,null=True,blank=True) 
     pincode=models.CharField(max_length=100,null=True,blank=True) 

     class Meta:
        verbose_name="Billing Address"
        verbose_name_plural="Billing Addresses"   

     def __str__(self):
        return self.user_id.email    