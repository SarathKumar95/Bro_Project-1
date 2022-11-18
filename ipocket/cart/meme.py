from django.shortcuts import render
from django.http import JsonResponse 
import json
# Create your views here. 

def Add_To_Cart(request):
    data = json.loads(request.data) 
    productId = data['productId'] 
    action = data['action']

    print('Action:',action) 
    print('ProductId:',productId) 

    return JsonResponse('Item was added!',safe=False) 

