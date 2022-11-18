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

