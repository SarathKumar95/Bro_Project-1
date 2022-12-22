import os
import random
import json
from django.shortcuts import render, redirect

from ipocket import settings
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from category.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from cart.models import *
from category.forms import *
from ipocket.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET
from django.views.decorators.cache import cache_control
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.views.generic import View 
from twilio.rest import Client 
from ipocket.settings import account_sid,auth_token 
from indian_cities.dj_city import cities 


import razorpay

client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))


# global vars here

orderid = 0
grandTotal_after_discount = 0
coupon_check = 0
coupon_discount = 0
already_applied_coupon = "None"

# Create your views here.
def guest(request):
    guest_user = request.session.session_key

    if not guest_user:
        guest_user = request.session.create()

    print("User in is", guest_user)
    return guest_user


def home_page(request):
    category = Categories.objects.all()
    subcat = ProductType.objects.all()
    product = Products.objects.all()
    context = {'product': product, 'category': category, 'subcat':subcat}
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



#OTP login
def signinOTP(request):  
    if request.method == "POST":
        phone_number = request.POST.get('phone')
        
        if len(phone_number) < 12:             
            messages.info(request,"Enter a phone number with country code")
            return redirect(request.path)
        else:
            client = Client(account_sid,auth_token)

            # service = client.verify.v2.services.create(
            #                                 friendly_name='My First Verify Service'
            #                             )

            # print(service.sid)


            verification = client.verify \
                        .v2 \
                        .services('VAb89bd4d0748fe2f04b91cdd353fb0429') \
                        .verifications \
                        .create(to=phone_number, channel='whatsapp')

            print(verification.sid)

            return redirect('VerifyOTP/'+phone_number)

    return render(request, 'user/signinOTP.html')


def verifyOTP(request,phone):

    phone1 = "+"+str(phone)
    print("Phone is ",phone1)
    client = Client(account_sid,auth_token) 

    user_in = MyUser.objects.filter(mobile_number=phone1)

    print("user is", user_in)

    # for item in user_in[0]:
    #     print(item.email)   
    
    if request.method == 'POST':
        otp = request.POST.get("otp")

        print("Otp entered is", otp)

        verification_check = client.verify \
                           .v2 \
                           .services('VAb89bd4d0748fe2f04b91cdd353fb0429') \
                           .verification_checks \
                           .create(to=phone1,code=otp)

        print(verification_check.status)

        if verification_check.status == 'approved':
            mobile_number = phone1
            user = authenticate(request,mobile_number=mobile_number) 
            
            print("Reaching here",user) 

            if user is not None:
                print("user not none")
                
                for item in user_in:
                    email = item.email
                    
                request.session['username'] = email
                return redirect('home')

            else:
                messages.error(request,"Check phone number!")    

        else:
            messages.error(request, "Invalid OTP")    

    return render(request,'user/Otpverify.html')


def signout(request):
    if 'username' in request.session:
        request.session.flush()
        return redirect('/')


def myaccount(request):
    if 'username' in request.session:
        user_in = request.session['username']
        user_name=MyUser.objects.filter(email=user_in).first() 
        fname = user_name.first_name
        lname = user_name.last_name
        context = {'user_in': user_in, 'fname' : fname, 'lname': lname}
        return render(request, 'user/userhome.html', context)
    return redirect('signin')


def personal(request):
    if 'username' in request.session:
        user_in = request.session['username']
        user_name=MyUser.objects.filter(email=user_in).first() 
        fname = user_name.first_name
        lname = user_name.last_name 

        billAddress=BillingAddress.objects.filter(user_id=user_name.id).first() 

        print("Bill address is ", billAddress)        


        form=CustomUserChangeForm(instance=user_name)

        if request.method == 'POST':
            form=CustomUserChangeForm(request.POST, instance=user_name)

            if form.is_valid():
                messages.info(request,"Updated Successfully!")
                form.save()    
            else:
                for error in form.errors:
                    messages.error(request,error)     


        context = {'user_in': user_in, 'fname' : fname, 'lname': lname, 'form':form}
    return render(request,'user/personal.html',context)



def manage_address(request):
    if 'username' in request.session:
        user_in = request.session['username']
        user_name=MyUser.objects.filter(email=user_in).first() 
        fname = user_name.first_name
        lname = user_name.last_name 

        billAddress=BillingAddress.objects.filter(user_id=user_name.id).first()


        Billform=BillingAddressForm(instance=billAddress) 

        if request.method=='POST':
            Billform=BillingAddressForm(request.POST,instance=billAddress) 
            if Billform.is_valid():
                Billform.save()
                messages.success(request, "Update Successful")  
            else:
                messages.success(request, Billform.errors)

    context = {'user_in': user_in, 'fname' : fname, 'lname': lname, 'Billform':Billform}
    return render(request,'user/manageaddress.html',context)




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
    
    if request.method == 'POST':

        #range = 
        
        if 'rangeprice' in request.POST:
            print("Range is",request.POST['rangeprice'])

        else:
            pass    

        if 'condition' in request.POST and 'productType' not in request.POST:
            condition_in = request.POST['condition']
            print("Condition is", condition_in)

            id_of_condition=Categories.objects.filter(condition=condition_in).first().category_id 

            print("Cat id is", id_of_condition)

            product = Products.objects.filter(condition=id_of_condition)
            messages.success(request,"Listing "+condition_in+" products") 

        elif 'productType' in request.POST and 'condition' not in request.POST:
            protype = request.POST['productType']
            
            print("Product Type is",protype)

            id_of_protype=ProductType.objects.filter(product_type=protype).first().sub_cat_id

            print("Product Type id is", id_of_protype)

            product = Products.objects.filter(product_type=id_of_protype)
            
            messages.success(request,"Listing "+protype) 


        elif 'condition' and 'productType' not in request.POST:
            messages.error(request,"Please select one condition and product type!") 

        
        else:
            condition = request.POST['condition']
            protype=request.POST['productType'] 

            print("Condition is",condition,"Protype is", protype)

            category_selected=Categories.objects.filter(condition=condition)
            subcategory=ProductType.objects.filter(product_type=protype)

            print("Category selected is",category_selected,"Product type is",subcategory)


            no_of_category = Categories.objects.filter(condition=condition).count()   
            no_of_subcategory=ProductType.objects.filter(product_type=protype).count()
        
            print("Count is ",no_of_category)
            print("Count is ",no_of_subcategory)
        
            if no_of_subcategory == 0:
                return redirect(request.path)

            else:
                for item in category_selected:
                    Cat_id = item.category_id 
                
                print("Cat id is", Cat_id)    

                for item in subcategory:
                    SubCat_id = item.sub_cat_id

                print("Sub Cat id is", SubCat_id)

                product=Products.objects.filter(condition=Cat_id,product_type=SubCat_id)   

                print("Products are",product)
        
    context = {'product': product, 'category': category,'subCategory': subCategory}
    return render(request, 'home/shop.html', context) 

#Filter Product 
def product_filter(request,Cat_id,Subcat_id):
    product = Products.objects.filter(condition=Cat_id,product_type=Subcat_id)  
    category = Categories.objects.all()
    subCategory = ProductType.objects.filter()
    context = {'product': product, 'category': category,
        'subCategory': subCategory}
    return render(request, 'home/shop.html')


def product_type_filter(request,typeid):
    product = Products.objects.filter(product_type=typeid)  
    category = Categories.objects.all()
    subCategory = ProductType.objects.all()
    context = {'product': product, 'category': category,
        'subCategory': subCategory}
    return render(request, 'home/shop.html', context)

#Sort Products 
#price 

def sortbyprice_ascending(request):
    product = Products.objects.order_by('price')  
    category = Categories.objects.all()
    subCategory = ProductType.objects.all()
    context = {'product': product, 'category': category,
        'subCategory': subCategory}
    return render(request, 'home/shop.html', context)
    


def sortbyprice_descending(request):
    product = Products.objects.order_by('-price')  
    category = Categories.objects.all()
    subCategory = ProductType.objects.all()
    context = {'product': product, 'category': category,
        'subCategory': subCategory}
    return render(request, 'home/shop.html', context)


def sortbynew(request):
    product = Products.objects.order_by('-created_at')  
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


            if (product_check):
                    if (Cart.objects.filter(user=email, product_id=product_id)):
                        print("Product already in cart")
                        return JsonResponse({'status': "Product already in cart"})

                    else:
                         if product_check.quantity >= product_quantity:
                            print("adding to cart")
                            Cart.objects.create(
                                user=email, product_id=product_id, product_qty=product_quantity)
                            return JsonResponse({'status': 'Product added succesfully'})

                         else:
                            return JsonResponse({'status': 'Only ' + str(product_check.quantity) + ' quantity is available.'})
            else:
                return JsonResponse({'status': "No such product found"})

    return redirect('/')


def cart_list(request):

    guest_cart = Cart.objects.filter(session_id=guest(request)).all()
    print("No of guest cart items are",guest_cart.count())

    if 'username' not in request.session:
        cart = Cart.objects.filter(session_id=guest(request))  
        
    elif 'username' in request.session:
        user_in = request.session['username']

        if guest_cart.count == 0:
            pass

        
        else:
            print("guest cart is present") 

            print("Guest cart is", guest_cart)

            for item in guest_cart:
                # if product in cart            
                if(Cart.objects.filter(user=user_in,product = item.product)):
                    print("True")
                    cart = Cart.objects.filter(user=user_in,product=item.product).first()  #itterate and get the product

                    cart.product_qty+=1 #increase its quantity
                    cart.save()          

                    print("The item which is in the cart is", cart, "The qty is", cart.product_qty) 

                    #item.product.delete() # delete that product from guest cart  
               

                else:
                    print("False")       #add the product

                    cart = Cart.objects.create(user=user_in,product=item.product,product_qty=item.product_qty) 
                    cart.save()

            cart = Cart.objects.filter(user = user_in)
            
            guest_cart.delete()

            #print the guest cart to know if its deleted 

            print("Guest cart after deleting the product is", guest_cart)  



    sub_total=0
    
    tax = 0
    for item in cart:
        product_qtyCheck=item.product.quantity
        
        if item.product.price_after_offer > 0:
            Item_total = item.product.price_after_offer * item.product_qty
        else:
            Item_total = item.product.price * item.product_qty
        
        sub_total+=Item_total

        print("Quantity is",product_qtyCheck)
        
        print("Sub total is",sub_total)    


    no_of_cart_items = cart.count()
    context = {'cart': cart,'no_of_cart_items':no_of_cart_items,'sub_total':sub_total}
        
    return render(request,'home/cartlist.html',context)    





def cart_update(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        product_qty = request.POST['cart_qty']
        cart_id=request.POST['cart_id']
        
        product=Products.objects.filter(product_id=product_id)
        
        print("Product Qty is",product_qty)   
        print("Cart Id is",cart_id)        
        

        if 'username' not in request.session:
            user_in = guest(request)
            cart = Cart.objects.filter(session_id=user_in,product=product_id).first() 

        else:
            user_in = request.session['username']
            cart = Cart.objects.filter(user=user_in,product=product_id).first() 
        
        
        
        
        CartTotal= Cart.objects.filter(user=user_in)
        
        print("Cart total is ",CartTotal)
        
        total=0
            
        for item in CartTotal:
            if item.product.price_after_offer > 0:
                itemPrice=item.product.price_after_offer
            else:
                itemPrice=item.product.price  
            
            print("Item price is", itemPrice)
            
            total= total + itemPrice 
            
            print("Total is",total)      
        
        if cart.product.price_after_offer > 0:
            cartPrice=cart.product.price_after_offer 
        else:
            cartPrice=cart.product.price    
        
        print("Cart product price is", cartPrice) 
        
        on_change_price = total - cartPrice  #minus the existing cart price from total
        
        update_price=on_change_price + (cartPrice * float(product_qty))
        
        print("Total to cart is",on_change_price) 
        
        print("Updated price is ", update_price)
        
        cart.product_qty = product_qty  
        cart.save()
        
        return JsonResponse({'status':'Updated cart!', 'update_price':update_price})

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


# Order page
def OrderPage(request,tracking_no):
    order = Order.objects.filter(tracking_no=tracking_no).filter(user=request.session['username']).all()     
    for item in order:
        orderid = item.id 
        orderitem = OrderItem.objects.filter(order_id = orderid).all()
        print("Order item is", orderitem)

    orderTotal=0

    for item in orderitem:
        # print("Item name is", item.product.price)
        orderTotal= orderTotal + item.product.price * item.quantity

    print("Order item total is",orderTotal)        

    context = {'order':order, 'orderitem':orderitem, 'orderTotal':orderTotal}
    return render(request,'home/orderplaced.html',context)




def order_manager(request):
    orders = Order.objects.all().order_by('created_at')
    context = {'orders':orders}
    return render(request,'owner/ordermanager.html',context)    


def order_edit(request, id):
    order = Order.objects.filter(id=id).first()
    orderitem = OrderItem.objects.filter(order_id=order.id).all()

    countOrderItem = orderitem.count()

    print("Order status is", order.status) 
    print("Order item is", orderitem)
    print("No of Order item is", countOrderItem)


    form = OrderForm(instance=order)

    print("Statuses in order is :" , order.orderstatus[1])  


    
    print("Status of order is", form['status']) 



    for item in orderitem:
        print("The order status before is", order.status, "The order item is",item.product.slug,"and the order item status before is", item.item_status)

    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
              
        for item in orderitem:
              item.item_status = request.POST['status'] 
              item.save()  
              print("The orderitem is",item.product.slug ," Order status after is", order.status, "and the order item status after is", item.item_status)

        if form.is_valid():
            form.save()
            messages.success(request,"Order Updated") 
            return redirect('order-list')
        else:
            messages.error(request,form.errors) 

    context = {'form':form, 'order':order, 'orderitem': orderitem} 
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

# Search view 

def search_product(request):
    if request.method == 'POST':
        product_searched = request.POST['searchPro'] 

        print(product_searched)

        if product_searched == " ":
            messages.error(request, "Insert something to search!")
            

        else:
            product = Products.objects.filter(slug__icontains = product_searched ).first()
            
            if product:
                return redirect('item/'+ str(product.product_id))

            else:
                messages.error(request, "Sorry, Your search does not match any products!")       

    return redirect('productspage') 

# Download invoice function


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html =template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result) 

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return None    


def viewInvoice(request,tracking_no):
    user_in = request.session['username']
    order = Order.objects.filter(user=user_in,tracking_no = tracking_no).first()
    orderitem = OrderItem.objects.filter(order = order)
    
    print("Order is ", order)
    print("Order item is ", orderitem)

    data = { 
            'order':order,
            'orderitem':orderitem     
        }

    pdf = render_to_pdf('user/invoice.html', data)
    return HttpResponse(pdf, content_type='application/pdf')



#Coupon views

def coupon_manager(request):
    coupons=Coupon.objects.all()
    form=CouponForm()
    context = {'coupons':coupons, 'form':form}
    return render(request,'owner/couponmanager.html',context)   



def coupon_add(request):
    form=CouponForm()
    context={'form':form} 

    if request.method == 'POST':
        form=CouponForm(request.POST)
        if form.is_valid():
            messages.success(request,"New Coupon Added!")
            form.save()
            return redirect('coupon-manager')
        else:
            print("Hit here!!")
            messages.error(request,form.errors)    
    return render(request,'owner/couponadd.html',context)



def coupon_editor(request,coupon_id):
    coupon=Coupon.objects.filter(coupon_id=coupon_id).first() 
    form=CouponForm(instance=coupon)
    context={'form':form} 

    if request.method=='POST':
        form=CouponForm(request.POST, instance=coupon) 

        
        if form.is_valid():
            form.save()
            messages.success(request,"Coupon Updated") 
            return redirect('coupon-manager')
        else:
            messages.error(request,form.errors) 

    return render(request,'owner/couponedit.html',context)   




def coupon_delete_admin(request,coupon_id):
    coupon=Coupon.objects.filter(coupon_id=coupon_id).first() 
    coupon.delete()
    messages.error(request, "Removed Coupon")
    return redirect('coupon-manager')




def coupon_all(request):
    coupons=Coupon.objects.all()
    data = list()
    for item in coupons:
        data.append(item.coupon_code)

    return JsonResponse(data, safe=False)    


def coupon_post(request):
    if request.method == 'POST':
        grandTotal= request.POST['grandTotal']
        coupon=request.POST['coupon'] 

        print("Type grand", type(grandTotal))
        
        cart=Cart.objects.filter(user=request.session['username']).first()

        print("Cart coupon is", cart.coupon_applied)

        global coupon_check
        coupon_check=Coupon.objects.filter(coupon_code=coupon).first()
        
        print("Coupon applied is", coupon_check)
        

        point_grand = float(grandTotal) 


        print("Type x is", type(point_grand))

        if coupon_check:
            print("STATUS IS", coupon_check.is_expired)
            
            if cart.coupon_applied == coupon:
                return JsonResponse({'status':"Coupon Already Applied!"})

            elif coupon_check.is_expired == False:

                if point_grand < coupon_check.minimum_amount:
                    return JsonResponse({'status':"Add items worth "+str(coupon_check.minimum_amount - point_grand)+" to avail this coupon"})
            

                elif point_grand > coupon_check.maximum_amount:
                         return JsonResponse({'status':"Coupon only applicable to orders below "+str(coupon_check.maximum_amount)})
                else:

                    coupon_perc=coupon_check.discount_percentage/100
                    global coupon_discount
                    coupon_discount= float(grandTotal) * coupon_perc 
                
                    global grandTotal_after_discount               
                    grandTotal_after_discount=float(grandTotal)-coupon_discount

                    print("Coup perc is",coupon_perc)

                    print("Price to be discounted is",coupon_discount)

                    print("Grand Total is",grandTotal_after_discount)

                    cart.coupon_applied=coupon
                    cart.coupon_discount=coupon_discount
                    cart.grand_total=grandTotal_after_discount
                    cart.save()

                    print("Coupon is passed to cart", cart.coupon_applied, "Coupon discount passed to cart", cart.coupon_discount )
                
                    return JsonResponse({'status':"Coupon Applied"})
    
            elif coupon_check.is_expired == True:
                return JsonResponse({'status':"Sorry,this coupon seems to be expired!"}) 


        else:
            return JsonResponse({'status':"Invalid Coupon"})
    

        return redirect('checkout')        


def coupon_delete(request):
    if request.method == 'POST':
        cart=Cart.objects.filter(user=request.session['username']).first()
        print("Cart is ", cart.coupon_applied) 

        cart.grand_total+=cart.coupon_discount
        cart.coupon_applied = None
        cart.coupon_discount = 0 
        cart.save()
        return redirect('checkout')



#Checkout
@cache_control(no_cache=True)
def checkout(request):
    if 'username' not in request.session:
        messages.info(request,"Please Login")
        return redirect('signin')
        
    user_in = request.session['username']
    cart = Cart.objects.filter(user = user_in)
    user_filt = MyUser.objects.filter(email=user_in) 

    print("Cart in checkout is ", cart) 

    kerala=["Thiruvananthapuram","Kochi","Calicut","Kollam","Thrissur","Kannur","Kasaragod","Alappuzha","Palakkad","Kottayam","Kothamangalam","Malappuram","Manjeri","Thalassery", "Ponnani",]

    for item in kerala:
        print("item is", item)


    sub_total = 0
    tax = 0

    cart_to_html=Cart.objects.filter(user=user_in).first()

    print("Cart coupon status is",cart_to_html.coupon_applied)    

    for item in cart:
        if item.product.price_after_offer > 0:
            Item_total = item.product.price_after_offer * item.product_qty
        else:    
            Item_total = item.product.price * item.product_qty
        
        
    sub_total+=Item_total 
    
    if sub_total <= 100000:
        shipping = 150
        
    else:
        shipping = 0       
        tax = 5

    
    grand_total_with_tax = sub_total * tax/100

    
    if cart_to_html.grand_total:
        grand_total = cart_to_html.grand_total
        print("Grand total from cart is", cart_to_html.grand_total)

    else:
         grand_total = sub_total + shipping + grand_total_with_tax     
    
    
   


    print("Sub total is",sub_total)
    print("Shipping is",shipping)
    print("Tax is",tax) 
    print("Tax amount is",grand_total_with_tax)
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
            
            if coupon_discount:
                neworder.total_price = grand_total - coupon_discount
                neworder.coupon_amount = coupon_discount
            else:
                neworder.total_price = grand_total
                neworder.coupon_amount = 0    
            

            
            neworder.price_before_tax = sub_total 
            neworder.tax_amount = grand_total_with_tax
            neworder.ship_amount = shipping
            neworder.payment_mode = request.POST['paymentMethod'] 


            print("New order sub total is", neworder.price_before_tax) 




            print("The payment mode used is ", request.POST['paymentMethod'])


            track_no = 'IPOrder' + str(random.randint(111111,999999)) 
            while Order.objects.filter(tracking_no=track_no) is None:
                track_no = 'IPOrder' + str(random.randint(111111,999999))

            neworder.tracking_no = track_no
            neworder.coupon=cart_to_html.coupon_applied
            
            neworder.save() 


            neworderItems = Cart.objects.filter(user=user_in)

            print("ITEMS IN THE CART ARE",neworderItems)

            print("NO OF ITEMS IN CART",neworderItems.count())


            for item in neworderItems:
                OrderItem.objects.create(
                    order = neworder,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.product_qty

                )

                
                print("Item added is",item.product.slug)
                print("Item price added is",item.product.price)
                print("Item qty added is",item.product_qty)


                orderproduct = Products.objects.filter(product_id=item.product.product_id).first()
                
                print("Ordered product is",orderproduct.slug,"and quantity is", orderproduct.quantity) 
                orderproduct.quantity -= item.product_qty 
                orderproduct.save()
                print("Ordered product quantity after ordering is", orderproduct.quantity) 

                
                cart = Cart.objects.filter(user=user_in) 
                cart.delete()     
                
            if request.POST['paymentMethod'] != "Cash On Delivery":
                return JsonResponse({"track_no" : track_no })

            else:
                return redirect('order-page',tracking_no=neworder.tracking_no)     
            
    context = {'user_filt':user_filt,'cart':cart,'cart_to_html':cart_to_html,'sub_total':sub_total,'shipping':shipping, 'tax':tax, 'grand_total_with_tax':grand_total_with_tax, 'grand_total':grand_total, 'api_key' : RAZOR_KEY_ID}    
    return render(request,'home/checkout.html',context) 




