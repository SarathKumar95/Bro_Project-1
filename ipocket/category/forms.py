from django.forms import ModelForm,TextInput,NumberInput,Select,Textarea,FileInput
from django import forms
from category.models import *


class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = "__all__"
        widgets = {
            'product_name': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder' : "iPhone"
            }),

            'generation' : TextInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "12"

                }
            ),

            'series' : TextInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "Mini"

                }
            ),

            'color' : TextInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "Black"

                }
            ),

            'internal_storage' : TextInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "128GB"

                }
            ),

            'category' : Select(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "Phones"

                }
            ),

            'price' : NumberInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "₹50000"                   
                }
            ),

            'quantity': NumberInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "1"                   
                }
            ),

            'condition': TextInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "Used.Like New"
                }
            ),

            'description' : Textarea(
                attrs = {
                    'class':"form-control",
                    'style': "max-width: 300px;",
                }
            ),

        }

    def clean(self):
        quantity = self.cleaned_data["quantity"]
        price = self.cleaned_data["price"]
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be less than 0.") 
        elif price < 0:
            raise forms.ValidationError("Price cannot be less than 0.")

        
            




class CategoryForm(ModelForm):
    class Meta:
        model = Categories
        fields = "__all__"        