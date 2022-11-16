from django.shortcuts import render
from category.models import *
from django.http import HttpResponse
# Create your views here.

def cart_list(request):
    return render(request, 'cart/viewcart.html')

def cart_add(request,product_id): 
    product = Products.objects.get(product_id=product_id)
    return HttpResponse(product)
