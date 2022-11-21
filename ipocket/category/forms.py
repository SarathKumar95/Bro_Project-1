from django.forms import ModelForm,TextInput,NumberInput,Select,Textarea,FileInput
from django import forms
from category.models import *


class SubCategoryForm(ModelForm):
    
    class Meta:
        model = SubCategories
        fields = '__all__'



class CategoryForm(ModelForm):

    class Meta:
        model = Categories
        fields = '__all__'


class ProductForm(ModelForm):

    class Meta:
        model = Products
        fields = '__all__' 

