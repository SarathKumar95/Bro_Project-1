from django.forms import ModelForm
from category.models import *


class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = "__all__"