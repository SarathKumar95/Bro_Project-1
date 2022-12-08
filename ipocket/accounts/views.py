import random
import json
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from category.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from cart.models import *
from category.forms import *
import razorpay
from ipocket.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET
# Create your views here.
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))


# global vars here

orderid = 0;


def guest(request):
    guest_user = request.session.session_key

    if not guest_user:
        guest_user = request.session.create()

    print("User in is", guest_user)
    return guest_user


def home_page(request):
    category = Categories.objects.all()
    product = Products.objects.all()
    context = {'product': product, 'category': category}
    return render(request, 'home/index.html', context)


def register(request):
    form = CustomUserCreationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.info(request, "You are registered!Login Here.")
            return redirect('signin')
        else:
            messages.error(request, form.errors)

    return render(request, 'user/register.html', context)


def signin(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        request.session['username'] = email

        if user is not None and user.is_active == True:
            if user.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Check credentials or contact admin.')

    return render(request, 'user/signin.html')


def signout(request):
    if 'username' in request.session:
        request.session.flush()
        return redirect('/')


def myaccount(request):
    if 'username' in request.session:
        user_in = request.session['username']
        context = {'user_in': user_in}
        return render(request, 'user/userhome.html', context)
    return redirect('signin')


def myorder(request):
    global orderid

    if 'username' in request.session:
        user_in = request.session['username']
        order = Order.objects.filter(user=user_in)

        for item in order:
            orderid = item.id

        orderitem = OrderItem.objects.filter(order_id=orderid)

        print("Order item is", orderitem)

        context = {'user_in': user_in, 'order': order, 'orderitem': orderitem}
        return render(request, 'user/myorders.html', context)
    return redirect('signin')


def dashboard(request):
    if 'username' in request.session:
            return render(request, 'owner/dashboard.html')
    else:
        return redirect('signin')


def user_manager(request):
    if 'username' in request.session:
        users = MyUser.objects.all()
        no_of_users = MyUser.objects.filter().count()
        no_of_superuser = MyUser.objects.filter(is_superuser=True).count()
        no_of_filtered_users = no_of_users - no_of_superuser
        context = {'users': users,
            'no_of_filtered_users': no_of_filtered_users}
        return render(request, 'owner/usermanager.html', context)

    else:
        return redirect(request.path)


def block_user(request, id):
    blocked_user = MyUser.objects.get(id=id)
    blocked_user.is_active = False
    blocked_user.save()
    print("Blocked user is", blocked_user)
    print("Is active status of blocked user is", blocked_user.is_active)
    return redirect("usermanager")


def unblock_user(request, id):
    user_to_unblock = MyUser.objects.get(id=id)
    user_to_unblock.is_active = True
    user_to_unblock.save()
    print("Unblocked user is", user_to_unblock)
    print("Is active status of blocked user is", user_to_unblock.is_active)
    return redirect("usermanager")


def products(request):
    product = Products.objects.all()
    category = Categories.objects.all()
    subCategory = ProductType.objects.all()
    context = {'product': product, 'category': category,
        'subCategory': subCategory}
    return render(request, 'home/shop.html', context)


def item(request, product_id):
    product = Products.objects.filter(product_id=product_id)
    products = Products.objects.all()
    context = {'product': product, 'products': products}
    return render(request, 'home/shop-single.html', context)


def signin_Otp(request):
    pass


# Cart functions here

def cart_add(request):
    
    if request.method == 'POST':
        if 'username' not in request.session:
            prod_id = request.POST['product_id']
            prod_qty = request.POST['product_qty']
            product = Products.objects.filter(product_id=prod_id).first()
            print("Prod id is", prod_id)
            print("Prod qty is", prod_qty)
            

            cart = Cart.objects.filter(session_id=guest(request))

            for item in cart:
                cart_product_ID = item.product.product_id 
        

            #if same product in cart
            if (Cart.objects.filter(session_id=guest(request), product_id=prod_id)):
                    return JsonResponse({'status': "Product already in cart, Please increase the quantity from cart"})
            
            else:
                print("create guest cart")
                cart = Cart.objects.create(session_id=guest(
                    request), product_id=prod_id, product_qty=prod_qty)
                guest_cart = Cart.objects.filter(session_id=guest(request)).first()  
                
                print("Guest cart is", guest_cart.product.product_id)
            
                return JsonResponse({'status': 'Product added succesfully'})

        
        elif 'username' in request.session:
            email = request.session['username']
            product_id = request.POST['product_id']
            product_quantity = int(request.POST['product_qty'])
            product_check = Products.objects.get(product_id=product_id)
            print("Product name is ", product_check)
            print("Stock is", product_check.quantity)
            print("Price of the product is", product_check.price)
            print("Ordered qty is", product_quantity)


            #Check if the product in guest cart is present in user's cart.If yes, update its quantity , otherwise add it as a new product 
            #print("Guest cart is", guest_cart)

            if (product_check):
                    if (Cart.objects.filter(user=email, product_id=product_id)):
                        return JsonResponse({'status': "Product already in cart"})

                    else:
                         if product_check.quantity >= product_quantity:
                            Cart.objects.create(
                                user=email, product_id=product_id, product_qty=product_quantity)
                            return JsonResponse({'status': 'Product added succesfully'})

                         else:
                            return JsonResponse({'status': 'Only' + str(product_check.quantity) + 'quantity is available.'})
            else:
                return JsonResponse({'status': "No such product found"})

    return redirect('/')


def cart_list(request):

    guest_cart = Cart.objects.filter(session_id=guest(request))
    print("No of guest cart items are",guest_cart.count())

    if 'username' not in request.session:
        cart = Cart.objects.filter(session_id=guest(request))  
        
    elif 'username' in request.session:
        user_in = request.session['username']

        if guest_cart.count == 0:
            pass

        
        else:
            print("guest cart is present") 

            for item in guest_cart:
                guest_product = item.product.product_id
                guest_qty = item.product_qty
                print("The id of item in guest cart is", guest_product)
                print("Ordered qty is", guest_qty)

                # product_in_cart = Cart.objects.filter(user = user_in) 
                # print("User Cart before adding guest cart is", product_in_cart)   

            cart = Cart.objects.filter(user = user_in)
            #guest_cart.delete()


    sub_total = 0
    tax = 0
    for item in cart:
        Item_total = item.product.price * item.product_qty
        sub_total+=Item_total
        

    no_of_cart_items = cart.count()
    context = {'cart': cart,'no_of_cart_items':no_of_cart_items,'sub_total':sub_total}
        
    return render(request,'home/cartlist.html',context)    





def cart_update(request):
    if request.method == 'POST':
        product_id = request.POST.get('cart_id')
        product_qty = request.POST['cart_qty']
          
        if 'username' not in request.session:
            user_in = guest(request)
            cart = Cart.objects.filter(session_id=user_in,product=product_id).first() 

        else:
            user_in = request.session['username']
            cart = Cart.objects.filter(user=user_in,product=product_id).first() 
                
            
        cart.product_qty = product_qty 
        cart.save()
        
        return JsonResponse({'status':'Updated cart!'})

    return redirect('/')        

def cart_delete(request):
    if request.method=='POST':
        prod_id = int(request.POST['product_id'])

        if 'username' not in request.session:
                cart_item = Cart.objects.filter(session_id = guest(request), product_id=prod_id)
                cart_item.delete()        
                

        else:
            user_in = request.session['username']
            cart_item = Cart.objects.filter(user = user_in, product_id=prod_id)
            cart_item.delete()

        return JsonResponse({"status": "Deleted Product Successfully!"})        
    return redirect('cart-list')        


# Checkout page view 

def checkout(request):
    if 'username' not in request.session:
        messages.info(request,"Please Login")
        return redirect('signin')
        
    user_in = request.session['username']
    cart = Cart.objects.filter(user = user_in)
    user_filt = MyUser.objects.filter(email=user_in) 


    print("Cart in checkout is ", cart) 

    
    sub_total = 0
    tax = 0
    coupon = 0
    for item in cart:
        Item_total = item.product.price * item.product_qty
        sub_total+=Item_total
    
    if sub_total <= 100000:
        shipping = 150
        
    else:
        shipping = 0       
        tax = 5
    

    grand_total_with_tax = sub_total * tax/100
    grand_total = sub_total + shipping + grand_total_with_tax

    print("Sub total is",sub_total)
    print("Shipping is",shipping)
    print("Tax is",tax) 
    print("Tax amount is",grand_total_with_tax)
    print("Coupon is",coupon)
    print("Grand total is",grand_total) 
    if request.method == 'POST':
        
        if cart.count() == 0:
            messages.info( request, "Cannot create an order as the cart is empty!")
             
        else:
        
            neworder = Order()
            neworder.user = request.session['username']
            neworder.first_name = request.POST['fname']
            neworder.last_name = request.POST['lname']
            neworder.email = request.POST['email']
            neworder.phone = request.POST['phno'] 
            neworder.address = request.POST['add'] 
            neworder.city = request.POST['city']
            neworder.state = request.POST['state'] 
            neworder.pincode = request.POST['zip']
            neworder.total_price = grand_total
            neworder.price_before_tax = sub_total 
            neworder.tax_amount = grand_total_with_tax
            neworder.ship_amount = shipping
            neworder.coupon_amount = coupon
            neworder.payment_mode = request.POST['paymentMethod']


            print("The payment mode used is ", request.POST['paymentMethod'])


            track_no = 'IPOrder' + str(random.randint(111111,999999)) 
            while Order.objects.filter(tracking_no=track_no) is None:
                track_no = 'IPOrder' + str(random.randint(111111,999999))

            neworder.tracking_no = track_no
            neworder.save() 

            neworderItems = Cart.objects.filter(user=user_in)

            print("Items in cart are",neworderItems)

            print("No of Items in cart are",neworderItems.count())


            for item in neworderItems:
                OrderItem.objects.create(
                    order = neworder,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.product_qty

                )

                
                print("Item added is",item.product.product_name)
                print("Item price added is",item.product.price)
                print("Item qty added is",item.product_qty)


                orderproduct = Products.objects.filter(product_id=item.product.product_id).first()
                print("Ordered product quantity is", orderproduct.quantity) 
                orderproduct.quantity -= item.product_qty 
                orderproduct.save()
                print("Ordered product quantity after ordering is", orderproduct.quantity) 

                
                cart = Cart.objects.filter(user=user_in) 
                cart.delete()     
                
                return JsonResponse({"track_no" : track_no })
            
            return redirect('order-page',tracking_no=neworder.tracking_no)     
            
    context = {'user_filt':user_filt,'cart':cart,'sub_total':sub_total,'shipping':shipping, 'tax':tax, 'grand_total_with_tax':grand_total_with_tax, 'grand_total':grand_total, 'api_key' : RAZOR_KEY_ID,}    
    return render(request,'home/checkout.html',context) 


# Order page
def OrderPage(request,tracking_no):
    order = Order.objects.filter(tracking_no=tracking_no).filter(user=request.session['username']).all()     
    
    print("Order is",order) 

    for item in order:
        orderid = item.id 

    orderitem = OrderItem.objects.filter(order_id = orderid)

    print("Order item is", orderitem)

    context = {'order':order, 'orderitem':orderitem}
    return render(request,'home/orderplaced.html',context)




def order_manager(request):
    orders = Order.objects.all()
    context = {'orders':orders}
    return render(request,'owner/ordermanager.html',context)    


def order_edit(request, id):
    order = Order.objects.filter(id=id).first() 
    orderitem = OrderItem.objects.filter(order_id=order.id).first()

    print("Order is", order) 
    print("Order item is", orderitem)

    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order) 

        if form.is_valid():
            print("The order status before is", order.status, "The order item status before is", orderitem.item_status)
            orderitem.item_status = order.status
            print("The order status after is", order.status, "The order item status after is", orderitem.item_status)   
            form.save()
            messages.success(request,"Order Updated") 
            return redirect('order-list')
        else:
            messages.error(request,form.errors) 

    context = {'form':form, 'orderitem': orderitem} 
    return render(request,'owner/orderedit.html',context) 

def order_info(request, id):
    order = Order.objects.filter(id=id).first() 
    orderitem = OrderItem.objects.filter(order_id=order.id).all() 
    print("Order item is", orderitem)

    for item in orderitem:
        print("Product in order", item.product.product_name) 

    context = {'orderitem': orderitem} 
    return render(request,'owner/orderinfo.html',context) 



def order_delete(request, id):
    order = Order.objects.filter(id=id).first()  
    order.delete()
    messages.info(request, "Removed Order")
    return redirect('order-list')
    


def orderitem_delete(request,id):
    orderitem = OrderItem.objects.filter(id=id) 

    for item in orderitem:
        print("Item id is", item.id) 
        orderid = item.order.id

    print("Order id is", orderid)

    
    orderitem.delete()
    messages.info(request, "Removed Product")
    return redirect("order-info",id=orderid)    



def orderitem_cancel(request,id):
    orderitem = OrderItem.objects.filter(id=id) 

    for item in orderitem:
        status = item.item_status
        print("Item status is", status) 



    messages.info(request, "Removed Product")
    return HttpResponse(item)
    #return redirect("order-info",id=orderid)    




def orderitem_edit(request,id):
    print("Id is", id)
    orderitem = OrderItem.objects.filter(id=id).first() 
    
    form = OrderItemForm(instance=orderitem) 

    if request.method == 'POST':
        form = OrderItemForm(request.POST,instance=orderitem) 

        if form.is_valid():
            form.save() 
            messages.success(request,"Order Item updated")
            
        else:
            messages.error(request,form.errors)

    context = {'form':form}
    return render(request, 'owner/orderitemedit.html',context)


def ordered(request,id):
    orderitem = OrderItem.objects.filter(id=id)
    
    item = OrderItem.objects.filter(id=id).first()

    
    if request.method == 'POST':
        item.item_status = 'Cancelled' 
        item.save()

    context = {'orderitem':orderitem}
    return render(request,'user/myorderitems.html',context)


# def payment_complete(request):
#     print("Paypal view hit!")
#     body = json.loads(request.body)
#     print("body: ",body) 

#     cart = body['cartIn']

#     print("Cart is", cart)

#     return JsonResponse('Payment Completed!', safe=False) 


def razor_checkout(request):    
    DATA = {
        "amount": 10000,
        "currency": "INR",
        "receipt": "receipt#1",
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
    }
    payment_order = client.order.create(data=DATA)
    payment_order_id = payment_order['id']  

    context = {
        'amount' : DATA['amount'], 'api_key' : RAZOR_KEY_ID, 'order_id': payment_order_id
    }

    return render(request, 'home/rpay.html', context) 