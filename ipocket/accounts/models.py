from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts.managers import UserManager


class MyUser(AbstractUser):
    username = None
    email = models.CharField(max_length=50, unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
