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



class OrderItemForm(ModelForm):

    class Meta:
        model = OrderItem
        fields = '__all__'