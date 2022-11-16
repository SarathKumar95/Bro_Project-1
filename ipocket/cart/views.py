from django.shortcuts import render,redirect
from category.models import *
from cart.models import *
from django.http import HttpResponse
# Create your views here.

#cart_list
def cart_list(request):
    return render(request, 'cart/viewcart.html')


def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart    


#cart_add
def cart_add(request,product_id): 
    product = Products.objects.get(product_id=product_id) 
    
    try:
        cart = Cart.objects.get(cart_id =_cart_id(request)) # get the cart using the cart_id present in session
    
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart) 
        cart_item.quantity += 1
        cart_item.save() 

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product,quantity = 1, cart=cart)
        cart_item.save() 

    return HttpResponse(cart_item.product)
    exit    
    return redirect('cart_list')



