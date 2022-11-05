from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import MyUser
from phonenumber_field.formfields import PhoneNumberField


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    mobile_number = PhoneNumberField(region='IN')

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'mobile_number', 'email')
