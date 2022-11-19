from django.forms import ModelForm,TextInput,NumberInput,Select,Textarea,FileInput
from django import forms
from category.models import *

'''

class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = "__all__"
        widgets = {
            'product_name': TextInput(attrs={
                'class': "form-control text-primary",
                'style': "max-width: 300px;",
            }),

            'generation' : TextInput(
                attrs={
                    'class':"form-control text-primary",
                    'style': "max-width: 300px;",

                }
            ),

            'series' : TextInput(
                attrs={
                    'class':"form-control text-primary",
                    'style': "max-width: 300px;",

                }
            ),

            'color' : TextInput(
                attrs={
                    'class':"form-control text-primary",
                    'style': "max-width: 300px;",

                }
            ),

            'internal_storage' : TextInput(
                attrs={
                    'class':"form-control text-primary",
                    'style': "max-width: 300px;",

                }
            ),

            'category' : Select(
                attrs={
                    'class':"form-control text-primary",
                    'style': "max-width: 300px;",
                }
            ),

            'price' : NumberInput(
                attrs={
                    'class':"form-control text-primary",
                    'style': "max-width: 300px;",                  
                }
            ),

            'quantity': NumberInput(
                attrs={
                    'class':"form-control text-primary",
                    'style': "max-width: 300px;",                   
                }
            ),

            'condition': TextInput(
                attrs={
                    'class':"form-control text-primary",
                    'style': "max-width: 300px;",
                }
            ),


             'brand' : TextInput(
                attrs = {
                    'class':"form-control text-primary",
                    'style': "max-width: 300px;",
                }
            ),

            'description' : Textarea(
                attrs = {
                    'class':"form-control text-primary",
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


'''
