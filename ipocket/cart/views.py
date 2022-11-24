from django.shortcuts import redirect, render
from django.http import JsonResponse
from category.models import *
from cart.models import *
# Create your views here.

def cart_list(request):
    return render(request,'home/cartlist.html')

