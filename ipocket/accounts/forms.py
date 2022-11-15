from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, TextInput
from .models import MyUser
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumber

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'style': 'width: 300px; height:30px;',
                                                                                             'class': 'form-control'
                                                                                             }))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'style': 'width: 300px; height:30px;',
                                                                                            'class': 'form-control'
                                                                                            }))

    mobile_number = PhoneNumberField(region='IN') 

    email = forms.EmailField(widget=forms.EmailInput(attrs={'style': 'width: 300px; height:30px;',
                                                            'class': 'form-control'
                                                            }))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'style': 'width: 300px; height:30px;',
            'class': 'form-control'

        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'style': 'width: 300px; height:30px;',
            'class': 'form-control'

        }
    ))

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'mobile_number', 'email')
