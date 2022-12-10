from django.forms import ModelForm,TextInput,NumberInput,Select,Textarea,FileInput
from django import forms
from category.models import *


class ProductTypeForm(ModelForm):
    
    class Meta:
        model = ProductType
        fields = '__all__'



class CategoryForm(ModelForm):

    class Meta:
        model = Categories
        fields = '__all__' 


class ProductForm(ModelForm):

    class Meta:
        model = Products
        fields = '__all__'
    

class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = '__all__'

        widgets= {
            'user': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'first_name': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'last_name': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'email': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'phone': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'address': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'state': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'city': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'pincode': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'total_price': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'tax_amount' : TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'ship_amount': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            
            'coupon_amount': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),

            
            'payment_mode': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            
            'price_before_tax': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),

            'payment_id': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }
            ),
            
            'tracking_no': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }
            ),

            'message' : Textarea(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),

            
            'status' : Select(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            })

            
            
            
        }



class OrderItemForm(ModelForm):

    class Meta:
        model = OrderItem
        fields = '__all__' 

        widgets= {
            'order': Select(attrs={
                'class': "form-control  text-dark",
                'style' : "max-width: 300px",
            }),            
            'product': Select(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),            
            'price': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),            
            'quantity': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),            
            
             'item_status': Select(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
        }
