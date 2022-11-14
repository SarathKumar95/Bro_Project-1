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
                'placeholder' : "Product Name : "
            }),

            'generation' : TextInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "Generation :"

                }
            ),

            'series' : TextInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "Series :"

                }
            ),

            'color' : TextInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "Color :"

                }
            ),

            'internal_storage' : TextInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "Generation :"

                }
            ),

            'category' : Select(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "Category :"

                }
            ),

            'price' : NumberInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "Price :"                   
                }
            ),

            'quantity': NumberInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                    'placeholder' : "Quantity :"                   
                }
            ),

            'condition': TextInput(
                attrs={
                    'class':"form-control",
                    'style': "max-width: 300px;",
                }
            ),

            'description' : Textarea(
                attrs = {
                    'class':"form-control",
                    'style': "max-width: 300px;",
                }
            ),

        }


class CategoryForm(ModelForm):
    class Meta:
        model = Categories
        fields = "__all__"        