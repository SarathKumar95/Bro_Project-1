import random
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from category.models import *
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse 
from cart.models import *
from category.forms import *
# Create your views here.

def home_page(request):
    category = Categories.objects.all()
    product = Products.objects.all()
    context = {'product':product,'category':category}
    return render(request,'home/index.html',context)


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
        context = {'user_in':user_in}
        return render(request, 'user/userhome.html',context)
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
        context = {'users': users , 'no_of_filtered_users': no_of_filtered_users}
        return render(request,'owner/usermanager.html',context)

    else:
        return redirect(request.path)


def block_user(request,id):
    blocked_user = MyUser.objects.get(id=id)
    blocked_user.is_active = False
    blocked_user.save()
    print("Blocked user is",blocked_user)
    print("Is active status of blocked user is",blocked_user.is_active)
    return redirect("usermanager")

def unblock_user(request,id):
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
    context = {'product':product, 'category':category, 'subCategory':subCategory}
    return render(request,'home/shop.html',context)


def item(request,product_id):
    product = Products.objects.filter(product_id=product_id)
    products = Products.objects.all()
    context = {'product':product,'products':products}    
    return render(request,'home/shop-single.html',context)

def signin_Otp(request):
    pass 



def cart_add(request):
    if request.method == 'POST':
        if 'username' not in request.session:
            return redirect('guest-add')

        elif 'username' in request.session:   
            email = request.session['username']
            product_id = request.POST['product_id']
            product_quantity = int(request.POST['product_qty'])
            product_check = Products.objects.get(product_id=product_id) 
            print("Product name is ", product_check)
            print("Stock is", product_check.quantity)
            print("Price of the product is", product_check.price)
            print("Ordered qty is",product_quantity)

            if(product_check):
                    if(Cart.objects.filter(user=email,product_id=product_id)):
                        return JsonResponse({'status':"product already in cart"})         

                    else:  
                         if product_check.quantity >= product_quantity:
                            Cart.objects.create(user=email,product_id=product_id,product_qty=product_quantity)
                            return JsonResponse({'status':'Product added succesfully'})

                         else:
                            return JsonResponse({'status':'Only' + str(product_check.quantity) + 'quantity is available.'})       
            else:
                return JsonResponse({'status':"No such product found"})    

        else:

            return JsonResponse({'status': "Login to continue"})    
            
    return redirect('/')    



def cart_list(request):
    user_in = request.session['username']
    cart = Cart.objects.filter(user = user_in)
    user_filt = MyUser.objects.filter(email=user_in) 

    
    sub_total = 0
    tax = 0
    for item in cart:
        Item_total = item.product.price * item.product_qty
        sub_total+=Item_total
    

    no_of_cart_items = cart.count()
    context = {'cart': cart,'no_of_cart_items':no_of_cart_items,'sub_total':sub_total}
    
    return render(request,'home/cartlist.html',context)

def cart_delete(request):

    user_in = request.session['username']
    if request.method=='POST':
        prod_id = int(request.POST['product_id'])
        if(Cart.objects.filter(user=user_in,product_id=prod_id)):
            cart_item = Cart.objects.filter(product_id=prod_id,user=user_in)
            cart_item.delete()
        return JsonResponse({"status": "Deleted Product Successfully!"})  
    return redirect('cart-list')        






# Checkout page view 

def checkout(request):
    user_in = request.session['username']
    cart = Cart.objects.filter(user = user_in)
    user_filt = MyUser.objects.filter(email=user_in) 

    
    sub_total = 0
    tax = 0
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


    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.session['username']
        neworder.first_name = request.POST['fname'] 
        neworder.last_name = request.POST['lname']
        neworder.email = request.POST['email']
        neworder.phone = request.POST['phno'] 
        neworder.address_line1 = request.POST['add1'] 
        neworder.address_line2 = request.POST['add2']
        neworder.city = request.POST['country']
        neworder.state = request.POST['state']
        neworder.pincode = request.POST['zip']
        neworder.total_price = grand_total
        neworder.payment_mode = request.POST['paymentMethod']
         

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

        return redirect('order-page',tracking_no=neworder.tracking_no)    
            
    context = {'user_filt':user_filt,'cart':cart,'sub_total':sub_total,'shipping':shipping, 'tax':tax, 'grand_total_with_tax':grand_total_with_tax, 'grand_total':grand_total}    
    return render(request,'home/checkout.html',context) 


#guest-cart-add 

def guestAdd(request):
    pass    




def order_manager(request):
    orders = Order.objects.all()
    context = {'orders':orders}
    return render(request,'owner/ordermanager.html',context)    


def order_edit(request, id):
    order = Order.objects.filter(id=id).first() 
    orderitem = OrderItem.objects.filter(order_id=order.id).first() 
    print("Ordered item is",orderitem.id)

    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order) 

        if form.is_valid():
            form.save()
            messages.success(request,"Order Updated") 
            return redirect('order-list')
        else:
            messages.error(request,form.errors) 

    context = {'form':form} 
    return render(request,'owner/orderedit.html',context) 


def OrderPage(request,tracking_no):
    order = Order.objects.filter(tracking_no=tracking_no).filter(user=request.session['username'])
     
    for item in order:
        order_id = item.id
        total = item.total_price 

    
    if total <= 100000:
        shipping = 150
        tax = 0
        discount = 0 
    else:
        shipping = 0       
        tax = 5
        discount = 0


    total_before_deductions = total - shipping - tax - discount
    tax_amount = (total - discount + shipping) * tax/100
    grand_total = total + shipping + tax_amount 

    print("Order ID is", order_id)

    print("Total - Ship - tax is", total)
    print("Tax amount is", tax_amount)
    print("Shipping amount is", shipping)
    
    orderitem = OrderItem.objects.filter(order_id = order_id)

    print("Order item is", orderitem)

    
    for item in orderitem:
        print(item.product.product_name, item.product.generation, item.product.series )

    context = {'order':order, 'orderitem':orderitem,'total':total_before_deductions,'tax_amount':tax_amount,'shipping':shipping,
     'discount':discount, 'grand_total':grand_total}
    return render(request,'home/orderplaced.html',context)

