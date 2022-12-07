from cart.models import * 


def cart_count(request):
    if 'username' not in request.session:
        cart = Cart.objects.filter(user=request.session.session_key) 
    else:
       cart = Cart.objects.filter(user=request.session['username'])    

    countCart = cart.count() 

    return dict({'countCart' : countCart})

