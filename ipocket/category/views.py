from django.shortcuts import render
from django.http import HttpResponse
from category.models import *

# Create your views here.

def product_manager(request):
    items = Products.objects.all()
    print(items)
    context = {'items': items}
    return render(request,'owner/productmanager.html',context)
