from django.forms import ModelForm
from django import forms
from category.models import *


class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = "__all__"


class CategoryForm(ModelForm):
    class Meta:
        model = Categories
        fields = "__all__"        