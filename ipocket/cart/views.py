from django.shortcuts import render,redirect,get_object_or_404
from category.models import *
from cart.models import *
from accounts.models import *
from django.http import HttpResponse
# Create your views here.

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

    print("The item is : " , cart_item.product , "The quantity of item is ", cart_item.quantity)
    #exit    
    return redirect('cart-list')


#cart_list
def cart_list(request,total=0,quantity=0,cart_items=None,no_of_items=0): 
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True) 
        no_of_items = CartItem.objects.filter(cart=cart, is_active=True).count()
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) 
            quantity += cart_item.quantity
            #print("The cart item is", cart_item.product)
            #print("The number of items in the cart is", no_of_items)
            #print("Id of cart item is", cart_item.id)
            #print("Cart items is",cart_item.product.product_name,cart_item.product.generation, "and the quantity is", cart_item.quantity)
            
    except Cart.DoesNotExist:   
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'no_of_items' : no_of_items,
    }

    
    # delivery cost

    standard_delivery = 50
    two_day_delivery = 130
    one_day_delivery = 300

    return render(request, 'cart/viewcart.html', context)


def remove(request,product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Products, product_id = product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart) 

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete() 
    return redirect('cart-list')        
    
# order confirmation 
def Order_Confirm(request,total = 0,quantity=0):
    if 'username' in request.session:
        cart = Cart.objects.get(cart_id = _cart_id(request)) 
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        no_of_items = CartItem.objects.filter(cart=cart, is_active=True).count()
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) 
            quantity += cart_item.quantity

        context = {'cart_items': cart_items, 'total' : total}

        return render(request,'cart/orderconfirmed.html',context) 

    else:
        return redirect('signin')