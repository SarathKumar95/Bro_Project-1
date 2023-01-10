import os
import random
import json
from django.shortcuts import render, redirect

from ipocket import settings
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
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
from ipocket.settings import account_sid, auth_token
from datetime import date
from accounts.models import *
from django.utils.dateparse import parse_date
import sys
import pandas as pd
from bs4 import BeautifulSoup
from django.db.models import Min,Max

import razorpay
import calendar


client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))


# global vars here

orderid = 0
grandTotal_after_discount = 0
coupon_check = 0
item_count_on_couponAdd = 0


# Create your views here.
def guest(request):
    guest_user = request.session.session_key

    if not guest_user:
        guest_user = request.session.create()

    print("User in is", guest_user)
    return guest_user


def home_page(request):
    check_user=False
    if 'username' in request.session:
        user_in = request.session['username'] 
        check_user = MyUser.objects.filter(email=user_in).first().is_superuser 
    else:
        pass    
    category = Categories.objects.all()
    subcat = ProductType.objects.all()
    product = Products.objects.all()
    banner = Banner.objects.all()

    banner_count=len(Banner.objects.all())

    print("Banner count is ", banner_count)

    context = {"product": product, "category": category, "subcat": subcat, 'check_user':check_user, 'banner':banner, 'banner_count':banner_count}
    return render(request, "home/index.html", context)


def register(request):
    form = CustomUserCreationForm()
    context = {"form": form}

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.info(request, "You are registered!Login Here.")
            return redirect("signin")
        else:
            messages.error(request, form.errors)

    return render(request, "user/register.html", context)


def signin(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)
        request.session["username"] = email

        if user is not None and user.is_active == True:
            if user.is_superuser:
                return redirect("dashboard")
            else:
                return redirect("home")
        else:
            messages.error(request, "Check credentials or contact admin.")

    return render(request, "user/signin.html")


# OTP login
def signinOTP(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone")

        if len(phone_number) < 12:
            messages.info(request, "Enter a phone number with country code")
            return redirect(request.path)
        else:
            client = Client(account_sid, auth_token)

            # service = client.verify.v2.services.create(
            #                                 friendly_name='My First Verify Service'
            #                             )

            # print(service.sid)

            verification = client.verify.v2.services(
                "VAb89bd4d0748fe2f04b91cdd353fb0429"
            ).verifications.create(to=phone_number, channel="whatsapp")

            print(verification.sid)

            return redirect("VerifyOTP/" + phone_number)

    return render(request, "user/signinOTP.html")


def verifyOTP(request, phone):

    phone1 = "+" + str(phone)
    print("Phone is ", phone1)
    client = Client(account_sid, auth_token)

    user_in = MyUser.objects.filter(mobile_number=phone1)

    print("user is", user_in)

    # for item in user_in[0]:
    #     print(item.email)

    if request.method == "POST":
        otp = request.POST.get("otp")

        print("Otp entered is", otp)

        verification_check = client.verify.v2.services(
            "VAb89bd4d0748fe2f04b91cdd353fb0429"
        ).verification_checks.create(to=phone1, code=otp)

        print(verification_check.status)

        if verification_check.status == "approved":
            mobile_number = phone1
            user = authenticate(request, mobile_number=mobile_number)

            print("Reaching here", user)

            if user is not None:
                print("user not none")

                for item in user_in:
                    email = item.email

                request.session["username"] = email
                return redirect("home")

            else:
                messages.error(request, "Check phone number!")

        else:
            messages.error(request, "Invalid OTP")

    return render(request, "user/Otpverify.html")


def signout(request):
    if "username" in request.session:
        request.session.flush()
        return redirect("/")


def myaccount(request):
    if "username" in request.session:
        user_in = request.session["username"]
        user_name = MyUser.objects.filter(email=user_in).first()
        fname = user_name.first_name
        lname = user_name.last_name
        context = {"user_in": user_in, "fname": fname, "lname": lname}
        return render(request, "user/userhome.html", context)
    return redirect("signin")


def personal(request):
    if "username" in request.session:
        user_in = request.session["username"]
        user_name = MyUser.objects.filter(email=user_in).first()
        fname = user_name.first_name
        lname = user_name.last_name

        billAddress = BillingAddress.objects.filter(user_id=user_name.id).first()

        print("Bill address is ", billAddress)

        form = CustomUserChangeForm(instance=user_name)

        if request.method == "POST":
            form = CustomUserChangeForm(request.POST, instance=user_name)

            if form.is_valid():
                messages.info(request, "Updated Successfully!")
                form.save()
            else:
                for error in form.errors:
                    messages.error(request, error)

        context = {"user_in": user_in, "fname": fname, "lname": lname, "form": form}
    return render(request, "user/personal.html", context)


def manage_address(request):
    user_in = request.session["username"]

    userID = MyUser.objects.filter(email=user_in).first().id

    if request.method == "POST":

        addressline = request.POST["addressline"]
        city = request.POST["city"]
        state = request.POST["state"]
        pincode = request.POST["pincode"]

        billingAddress.save()

        print("Created billing address ", billingAddress)

    return render(request, "user/manageaddress.html")


def myorder(request):
    global orderid

    if "username" in request.session:
        user_in = request.session["username"]
        order = Order.objects.filter(user=user_in)

        for item in order:
            orderid = item.id

        orderitem = OrderItem.objects.filter(order_id=orderid)

        print("Order item is", orderitem)

        context = {"user_in": user_in, "order": order, "orderitem": orderitem}
        return render(request, "user/myorders.html", context)
    return redirect("signin")


def dashboard(request):
    if "username" in request.session:

        todays_date = date.today()

        from_date = todays_date.replace(day=1)
        to_date = todays_date

        context = {
            "from_date": from_date,
            "to_date": to_date,
        }

        return render(request, "owner/dashboard.html", context)
    else:
        return redirect("signin")


def user_manager(request):
    if "username" in request.session:
        users = MyUser.objects.all()
        no_of_users = MyUser.objects.filter().count()
        no_of_superuser = MyUser.objects.filter(is_superuser=True).count()
        no_of_filtered_users = no_of_users - no_of_superuser
        context = {"users": users, "no_of_filtered_users": no_of_filtered_users}
        return render(request, "owner/usermanager.html", context)

    else:
        return redirect(request.path)


def block_user(request, id):
    blocked_user = MyUser.objects.get(id=id)
    blocked_user.is_active = False
    blocked_user.save()
    return redirect("usermanager")


def unblock_user(request, id):
    user_to_unblock = MyUser.objects.get(id=id)
    user_to_unblock.is_active = True
    user_to_unblock.save()
    return redirect("usermanager")


def products(request):
    product = Products.objects.all()
    category = Categories.objects.all()
    subCategory = ProductType.objects.all()


    #fetch max product price and min product price 

    max_product = ProductAttribute.objects.order_by('price').last().price      
    min_product = ProductAttribute.objects.order_by('-price').last().price
    
    if request.method == "POST":

        if 'price' in request.POST: 
            priceX = request.POST['price']
            productPrice = Products.objects.filter(price__lte = priceX) 

            if 'condition' in request.POST:
                conx = request.POST['condition']
                print("Condition is ", conx, "under ", priceX)
                messages.success(request,"Showing products filtered "+ conx + " under " + "₹ " 
                + priceX)

                id_of_condition = Categories.objects.filter(condition = conx).first().category_id
                product = productPrice.filter(condition_id = id_of_condition)
                productY = product
                if 'productType' in request.POST:
                    proX = request.POST['productType'] 
                    print("Condition is ",conx,"Pro type is ", proX, "under ", priceX)                    
                    id_of_pro = ProductType.objects.filter(product_type = proX).first().sub_cat_id
                    product = productY.filter(product_type_id=id_of_pro) 
            

            elif 'productType' in request.POST:
                proX = request.POST['productType'] 
                print("Pro type is ", proX, "under ", priceX)
                
                id_of_pro = ProductType.objects.filter(product_type = proX).first().sub_cat_id
                product = productPrice.filter(product_type_id=id_of_pro)  

        else:
            print("Nope!!")

    context = {"product": product, "category": category, "subCategory": subCategory, "max":max_product, "min":min_product}
    return render(request, "home/shop.html", context)


# Filter Product
def product_filter(request, Cat_id, Subcat_id):
    product = Products.objects.filter(condition=Cat_id, product_type=Subcat_id)
    category = Categories.objects.all()
    subCategory = ProductType.objects.filter()
    context = {"product": product, "category": category, "subCategory": subCategory}
    return render(request, "home/shop.html")


def product_type_filter(request, typeid):
    product = Products.objects.filter(product_type=typeid)
    category = Categories.objects.all()
    subCategory = ProductType.objects.all()
    context = {"product": product, "category": category, "subCategory": subCategory}
    return render(request, "home/shop.html", context)


# Sort Products
# price


def sortbyprice_ascending(request):
    product = Products.objects.order_by("price")
    category = Categories.objects.all()
    subCategory = ProductType.objects.all()
    context = {"product": product, "category": category, "subCategory": subCategory}
    return render(request, "home/shop.html", context)


def sortbyprice_descending(request):
    product = Products.objects.order_by("-price")
    category = Categories.objects.all()
    subCategory = ProductType.objects.all()
    context = {"product": product, "category": category, "subCategory": subCategory}
    return render(request, "home/shop.html", context)


def sortbynew(request):
    product = Products.objects.order_by("-created_at")
    category = Categories.objects.all()
    subCategory = ProductType.objects.all()
    context = {"product": product, "category": category, "subCategory": subCategory}
    return render(request, "home/shop.html", context)


def item(request, product_id):
    product = Products.objects.filter(product_id=product_id)
    product_attr = ProductAttribute.objects.filter(product_id=product_id) 

    price = product_attr.first().price
    image = product_attr.first().first_image
    first_pro = product_attr.first()

    products = Products.objects.all()
    context = {"product": product, "products": products,
    "product_attr":product_attr, "price":price,
    "image" : image,"first_pro":first_pro}
    return render(request, "home/shop-single.html", context)


# Cart functions here


def cart_add(request):

    if request.method == "POST":
        prod_id = request.POST["product_id"]
        pro_color = request.POST["color"] 
        prod_qty = 1

        pro_size = ProductAttribute.objects.filter(id=prod_id).first().size    

        print("User wants",pro_color, "pro size", pro_size)

        product_check = ProductAttribute.objects.filter(size=pro_size).filter(color=pro_color)

        if len(product_check) == 0:
            return JsonResponse({'status':"Sorry, that combination does not exist!"})

        else:

            if 'username' not in request.session:
                cart = Cart.objects.filter(session_id=guest(request))      

                #check if same product exists in cart 
                    
                if Cart.objects.filter(session_id=guest(request), product_attr_id=prod_id):
                    return JsonResponse({'status':"Product already in cart"}) 

                else:
                    cart = Cart.objects.create(session_id=guest(request), product_attr_id=prod_id, product_qty=prod_qty)
                    return JsonResponse({"status": "Product added succesfully"})

            elif 'username' in request.session:
                user_in = request.session['username'] 

                cart = Cart.objects.filter(user=user_in)      

                #check if same product exists in cart 
                    
                if Cart.objects.filter(user=user_in, product_attr_id=prod_id):
                    return JsonResponse({'status':"Product already in cart"}) 

                else:
                    cart = Cart.objects.create(user=user_in, product_attr_id=prod_id, product_qty=prod_qty)
                    return JsonResponse({"status": "Product added succesfully"})

                
    return redirect("/")

 
def cart_list(request):

    guest_cart = Cart.objects.filter(session_id=guest(request)).all()

    if "username" not in request.session:
        cart = Cart.objects.filter(session_id=guest(request))

    elif "username" in request.session:
        user_in = request.session["username"]

        if guest_cart.count == 0:
            pass

        else:

            for item in guest_cart:
                # if product in cart
                if Cart.objects.filter(user=user_in, product_attr=item.product_attr):
                    cart = Cart.objects.filter(
                        user=user_in, product_attr=item.product_attr
                    ).first()  # itterate and get the product

                    cart.product_qty += 1  # increase its quantity
                    cart.save()

                    # item.product.delete() # delete that product from guest cart

                else:
                    cart = Cart.objects.create(
                        user=user_in, product_attr=item.product_attr, product_qty=item.product_qty
                    )
                    cart.save()

            cart = Cart.objects.filter(user=user_in)

            guest_cart.delete()

    sub_total = 0

    tax = 0
    for item in cart:
        product_qtyCheck = item.product_attr.quantity

        if item.product_attr.price_after_offer > 0:
            Item_total = item.product_attr.price_after_offer * item.product_qty
        else:
            Item_total = item.product_attr.price * item.product_qty

        

        sub_total += Item_total

    no_of_cart_items = cart.count()
    context = {
        "cart": cart,
        "no_of_cart_items": no_of_cart_items,
        "sub_total": sub_total,
    }

    return render(request, "home/cartlist.html", context)


def cart_update(request):
    if request.method == "POST":
        product_id = int(request.POST["product_id"])
        product_qty = request.POST["cart_qty"]
        total = float(request.POST["total"])

        product = ProductAttribute.objects.filter(id=product_id).first() 

        if "username" not in request.session:
            user_in = guest(request)
            cart = Cart.objects.filter(session_id=user_in, product_attr_id=product_id).first()

        else:
            user_in = request.session["username"]
            cart = Cart.objects.filter(user=user_in, product_attr_id=product_id).first()
        

        CartTotal = Cart.objects.filter(user=user_in) 

        for item in CartTotal:
            
            if item.product_attr_id == product_id:
                   # minus the old price with old qty 
                   if item.product_attr.price_after_offer > 0:
                        price_to_Change = item.product_attr.price_after_offer * item.product_qty 
                        new_Price = item.product_attr.price_after_offer * float(product_qty) 
                   else:
                        price_to_Change = item.product_attr.price * item.product_qty 
                        new_Price = item.product_attr.price * float(product_qty)

                   total = total - price_to_Change + new_Price 
            else:
                pass        
    
        cart.product_qty = product_qty
        cart.save()

        return JsonResponse({"status": "Updated cart!", "update_price": total})

    return redirect("/")


def cart_delete(request):
    if request.method == "POST":
        prod_id = int(request.POST["product_id"])

        if "username" not in request.session:
            cart_item = Cart.objects.filter(
                session_id=guest(request), product_attr_id=prod_id
            )
            cart_item.delete()
        else:
            user_in = request.session["username"]
            cart_item = Cart.objects.filter(user=user_in, product_attr_id=prod_id)
            cart_item.delete()

        return JsonResponse({"status": "Deleted Product Successfully!"})
    return redirect("cart-list")


# Order page
def OrderPage(request, tracking_no):
    order = (
        Order.objects.filter(tracking_no=tracking_no)
        .filter(user=request.session["username"])
        .all()
    )
    for item in order:
        orderid = item.id
        orderitem = OrderItem.objects.filter(order_id=orderid).all()

    orderTotal = 0

    for item in orderitem:
        if item.product.price_after_offer:
            orderTotal = orderTotal + item.product.price_after_offer * item.quantity
        else:
            orderTotal = orderTotal + item.product.price * item.quantity

    context = {"order": order, "orderitem": orderitem, "orderTotal": orderTotal}
    return render(request, "home/orderplaced.html", context)


def order_manager(request):
    orders = Order.objects.all().order_by("-created_at")
    form = OrderForm()
    context = {"orders": orders, "form": form}

    if request.method == "POST":
        status = request.POST["status"]
        itemID = request.POST["itemID"]

        order = Order.objects.filter(id=itemID).first()

        orderItem = OrderItem.objects.filter(order_id=itemID).all()

        for item in orderItem:
            item.item_status = status
            item.save()

        order.status = status

        order.save()

    return render(request, "owner/ordermanager.html", context)


def order_edit(request, id):
    order = Order.objects.filter(id=id).first()
    orderitem = OrderItem.objects.filter(order_id=order.id).all()

    countOrderItem = orderitem.count()

    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)

        for item in orderitem:
            item.item_status = request.POST["status"]
            item.save()

        if form.is_valid():
            form.save()
            messages.success(request, "Order Updated")
            return redirect("order-list")
        else:
            messages.error(request, form.errors)

    context = {"form": form, "order": order, "orderitem": orderitem}
    return render(request, "owner/orderedit.html", context)


def order_info(request, id):
    order = Order.objects.filter(id=id).first()
    orderitem = OrderItem.objects.filter(order_id=order.id).all()

    context = {"orderitem": orderitem}
    return render(request, "owner/orderinfo.html", context)


def order_delete(request, id):
    order = Order.objects.filter(id=id).first()
    order.delete()
    messages.info(request, "Removed Order")
    return redirect("order-list")


def orderitem_delete(request, id):
    orderitem = OrderItem.objects.filter(id=id)

    for item in orderitem:
        orderid = item.order.id

    orderitem.delete()
    messages.info(request, "Removed Product")
    return redirect("order-info", id=orderid)


def orderitem_cancel(request, id):
    orderitem = OrderItem.objects.filter(id=id)

    for item in orderitem:
        status = item.item_status

    messages.info(request, "Removed Product")
    return HttpResponse(item)
    # return redirect("order-info",id=orderid)


def orderitem_edit(request, id):
    orderitem = OrderItem.objects.filter(id=id).first()

    form = OrderItemForm(instance=orderitem)

    if request.method == "POST":
        form = OrderItemForm(request.POST, instance=orderitem)

        if form.is_valid():
            form.save()
            messages.success(request, "Order Item updated")

        else:
            messages.error(request, form.errors)

    context = {"form": form}
    return render(request, "owner/orderitemedit.html", context)


def ordered(request, id):
    orderitem = OrderItem.objects.filter(id=id)

    item = OrderItem.objects.filter(id=id).first()

    if request.method == "POST":
        item.item_status = "Cancelled"
        item.save()

    context = {"orderitem": orderitem}
    return render(request, "user/myorderitems.html", context)


def razor_checkout(request):
    DATA = {
        "amount": 10000,
        "currency": "INR",
        "receipt": "receipt#1",
        "notes": {"key1": "value3", "key2": "value2"},
    }
    payment_order = client.order.create(data=DATA)
    payment_order_id = payment_order["id"]

    context = {
        "amount": DATA["amount"],
        "api_key": RAZOR_KEY_ID,
        "order_id": payment_order_id,
    }

    return render(request, "home/rpay.html", context)


# Search view


def search_product(request):
    if request.method == "POST":
        product_searched = request.POST["searchPro"]

        print(product_searched)

        if product_searched == " ":
            messages.error(request, "Insert something to search!")

        else:
            product = Products.objects.filter(slug__icontains=product_searched).first()

            if product:
                return redirect("item/" + str(product.product_id))

            else:
                messages.error(
                    request, "Sorry, Your search does not match any products!"
                )

    return redirect("productspage")


# Download invoice function


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")

    return None


def viewInvoice(request, tracking_no):
    user_in = request.session["username"]
    order = Order.objects.filter(user=user_in, tracking_no=tracking_no).first()
    orderitem = OrderItem.objects.filter(order=order)

    print("Order is ", order)
    print("Order item is ", orderitem)

    data = {"order": order, "orderitem": orderitem}

    pdf = render_to_pdf("user/invoice.html", data)
    return HttpResponse(pdf, content_type="application/pdf")


# Coupon views


def coupon_manager(request):
    coupons = Coupon.objects.all()
    form = CouponForm()
    context = {"coupons": coupons, "form": form}
    return render(request, "owner/couponmanager.html", context)


def coupon_add(request):
    form = CouponForm()
    context = {"form": form}

    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            messages.success(request, "New Coupon Added!")
            form.save()
            return redirect("coupon-manager")
        else:
            messages.error(request, form.errors)
    return render(request, "owner/couponadd.html", context)


def coupon_editor(request, coupon_id):
    coupon = Coupon.objects.filter(coupon_id=coupon_id).first()
    form = CouponForm(instance=coupon)
    context = {"form": form}

    if request.method == "POST":
        form = CouponForm(request.POST, instance=coupon)

        if form.is_valid():
            form.save()
            messages.success(request, "Coupon Updated")
            return redirect("coupon-manager")
        else:
            messages.error(request, form.errors)

    return render(request, "owner/couponedit.html", context)


def coupon_delete_admin(request, coupon_id):
    coupon = Coupon.objects.filter(coupon_id=coupon_id).first()
    coupon.delete()
    messages.error(request, "Removed Coupon")
    return redirect("coupon-manager")


def coupon_all(request):
    coupons = Coupon.objects.all()
    data = list()
    for item in coupons:
        data.append(item.coupon_code)

    return JsonResponse(data, safe=False)


def coupon_post(request):
    if request.method == "POST":
        grandTotal = request.POST["grandTotal"]
        coupon = request.POST["coupon"]

        cart = Cart.objects.filter(user=request.session["username"])

        itemcount = 0
        total = 0
        total_after_coupon = 0
        for item in cart:
            itemcount += 1
            itemCoupon = item.coupon_applied
            if item.product_attr.price_after_offer:
                price = item.product_attr.price_after_offer
            else:
                price = item.product_attr.price
            itemTotal = item.grand_total
            total += price

        coupon_check = Coupon.objects.filter(coupon_code=coupon).first()

        global item_count_on_couponAdd
        item_count_on_couponAdd = itemcount

        if coupon_check:

            if itemCoupon == coupon:
                return JsonResponse({"status": "Coupon Already Applied!"})

            elif coupon_check.is_expired == False:

                if total < coupon_check.minimum_amount:
                    return JsonResponse(
                        {
                            "status": "Add items worth "
                            + str(coupon_check.minimum_amount - total)
                            + " to avail this coupon"
                        }
                    )

                elif total > coupon_check.maximum_amount:
                    return JsonResponse(
                        {
                            "status": "Coupon only applicable to orders below "
                            + str(coupon_check.maximum_amount)
                        }
                    )
                else:

                    for item in cart:

                        item_Discount_to_apply = (
                            coupon_check.discount_percentage / itemcount
                        )

                        if item.product_attr.price_after_offer:
                            price = item.product_attr.price_after_offer
                        else:
                            price = item.product_attr.price

                        amount_to_be_discounted = price * item_Discount_to_apply / 100
                        price_after_discount = price - (
                            price * item_Discount_to_apply / 100
                        )

                        total_after_coupon = total_after_coupon + price_after_discount

                        if item.coupon_applied == None:
                            item.coupon_applied = coupon
                            item.discount_percentage = item_Discount_to_apply
                            item.amount_discounted = amount_to_be_discounted
                            item.grand_total = price_after_discount
                            item.save()

                        elif item.coupon_applied != None:
                            return JsonResponse(
                                {"status": "Only one coupon can be availed"}
                            )

                        elif coupon_check.is_expired == True:
                            return JsonResponse(
                                {"status": "Sorry,this coupon seems to be expired!"}
                            )

                    return JsonResponse(
                        {"status": "Coupon Applied", "total": total_after_coupon}
                    )

        else:
            return JsonResponse({"status": "Invalid Coupon"})

        return redirect("checkout")


def coupon_delete(request):
    cart = Cart.objects.filter(user=request.session["username"])

    for item in cart:
        if item.amount_discounted == None:
            item.grand_total = item.grand_total
        else:
            item.grand_total = item.grand_total + item.amount_discounted
            item.coupon_applied = None
            item.amount_discounted = 0
            item.discount_percentage = 0
            item.save()

    return JsonResponse({"status": "Removed Coupon"})


# Checkout
@cache_control(no_cache=True)
def checkout(request):
    if "username" not in request.session:
        messages.info(request, "Please Login")
        return redirect("signin")

    user_in = request.session["username"]
    cart = Cart.objects.filter(user=user_in)
    user_filt = MyUser.objects.filter(email=user_in)

    userID = MyUser.objects.filter(email=request.session["username"]).first().id

    customer_billAddress = BillingAddress.objects.filter(user_id=userID).first()
    customer_shipAddress = ShippingAddress.objects.filter(user_id=userID).first()

    if customer_billAddress == " " or customer_billAddress == " ":
        customer_billAddress = None

    else:
        pass

    if customer_shipAddress == None or customer_shipAddress == " ":
        customer_shipAddress = None

    else:
        pass

    sub_total = 0
    coupon_name = None
    total_discount = 0

    for item in cart:
        coupon_name = item.coupon_applied
        if item.product_attr.price_after_offer > 0:
            Item_total = item.product_attr.price_after_offer * item.product_qty
        else:
            Item_total = item.product_attr.price * item.product_qty
        sub_total += Item_total

        if item.amount_discounted != None:
            total_discount += item.amount_discounted
        else:
            pass

    cartAll = Cart.objects.filter(user=user_in)

    itemCount = len(cartAll)

    if cartAll[0].coupon_applied != cartAll[(itemCount - 1)].coupon_applied:
        coupon_delete(request)
        total_discount = 0
    else:
        pass

    if sub_total <= 100000:
        shipping = 150

    else:
        shipping = 0

    if total_discount != 0:
        grandTotal_with_shipping = sub_total + shipping - total_discount
    else:
        grandTotal_with_shipping = sub_total + shipping

    if request.method == "POST":

        if cart.count() == 0:
            messages.info(request, "Cannot create an order as the cart is empty!")

        else:
            if customer_billAddress == None:
                billAddress = BillingAddress()
                billAddress.user_id = userID
                billAddress.addressline = request.POST["billaddressline"]
                billAddress.city = request.POST["state"]
                billAddress.state = request.POST["city"]
                billAddress.pincode = request.POST["zip"]
                billAddress.save()

            elif request.POST["billaddressline"] == customer_billAddress.addressline:
                pass

                if request.POST.get("save-info", True):
                    shipAddress = ShippingAddress()
                    shipAddress.user_id = userID
                    shipAddress.addressline = request.POST["shipaddressline"]
                    shipAddress.city = request.POST["ship-city"]
                    shipAddress.state = request.POST["ship-state"]
                    shipAddress.pincode = request.POST["ship-zip"]
                    shipAddress.save()
                    print("Shipping address saved!")

                else:
                    pass

            neworder = Order()
            neworder.user = request.session["username"]
            neworder.first_name = request.POST["fname"]
            neworder.last_name = request.POST["lname"]
            neworder.email = request.POST["email"]
            neworder.phone = request.POST["phno"]
            neworder.address = request.POST["billaddressline"]
            neworder.city = request.POST["city"]
            neworder.state = request.POST["state"]
            neworder.pincode = request.POST["zip"]
            neworder.total_price = grandTotal_with_shipping

            if total_discount:
                neworder.coupon_amount = total_discount
            else:
                neworder.coupon_amount = 0

            neworder.ship_amount = shipping
            neworder.payment_mode = request.POST["paymentMethod"]

            track_no = "IPOrder" + str(random.randint(111111, 999999))
            while Order.objects.filter(tracking_no=track_no) is None:
                track_no = "IPOrder" + str(random.randint(111111, 999999))

            neworder.tracking_no = track_no
            neworder.coupon = coupon_name

            neworder.save()

            neworderItems = Cart.objects.filter(user=user_in)

            for item in neworderItems:
                price = item.product_attr.price
                # if item.product_attr.price_after_offer:
                #     price = item.product_attr.price_after_offer

                # else:
                    

                OrderItem.objects.create(
                    order=neworder,
                    product=item.product_attr,
                    price=price,
                    quantity=item.product_qty,
                )

                orderproduct = ProductAttribute.objects.filter(
                    id=item.product_attr_id
                ).first()

                orderproduct.quantity -= item.product_qty
                orderproduct.save()

                cart = Cart.objects.filter(user=user_in)
                cart.delete()

            if request.POST["paymentMethod"] != "Cash On Delivery":
                return JsonResponse({"track_no": track_no})

            else:
                return redirect("order-page", tracking_no=neworder.tracking_no)

    context = {
        "user_filt": user_filt,
        "cart": cart,
        "sub_total": sub_total,
        "shipping": shipping,
        "coupon_name": coupon_name,
        "total_discount": total_discount,
        "total": grandTotal_with_shipping,
        "api_key": RAZOR_KEY_ID,
        "customer_billAddress": customer_billAddress,
        "customer_shipAddress": customer_shipAddress,
    }
    return render(request, "home/checkout.html", context)


# Order Return


def returnOrder(request, itemID):
    orderID = itemID

    order = Order.objects.filter(id=orderID).first()

    orderItem = OrderItem.objects.filter(order_id=orderID).all()

    context = {"orderItem": orderItem, "order": order}

    if request.method == "POST":
        item = request.POST.getlist("item")
        order = request.POST["order"]

        IteminOrder = OrderItem.objects.filter(order_id=order).all().count()

        user_in = request.session["username"]

        userID = MyUser.objects.filter(email=user_in).first().id

        length_of_item = len(item)

        for itemid in item:
            orderItemID = OrderItem.objects.filter(id=itemid).first().id
            orderItem = OrderItem.objects.filter(id=itemid).first()
            orderItem.item_status = "Returned"
            orderItem.save()

            print("Order item is ", orderItemID)

            print("Order item quantity is ", orderItem.quantity)

            wallet = Wallet.objects.create(
                user_id=userID,
                orderItem_id=orderItemID,
                quantity=orderItem.quantity,
                amount=orderItem.price,
            )

            print("Wallet created ", wallet)

            if length_of_item == IteminOrder:

                get_order = Order.objects.filter(id=order).first()
                get_order.status = "Returned"
                print("Total of return is ", get_order.total_price)
                get_order.save()

        messages.info(request, "Return Confirmed! Our representative will contact you!")
    return render(request, "user/orderreturn.html", context)


def chart(request):
    labels = []
    ordered = [] 
    delivered = []
    returned = []
    cancelled = []

    order_total = 0    
    deliver_total = 0
    return_total = 0
    cancel_total = 0

    today_order = len(Order.objects.filter(created_at=date.today()))
    period_order = 0

    start = 1
    end = 31
    month = date.today().month
    year = date.today().year

    total_revenue = 0
    today_revenue = 0

    deliver_price = 0
    return_price = 0
    cancel_price = 0

    if request.method == 'POST':
        fromDate = parse_date(request.POST['fromDate']) 
        toDate = parse_date(request.POST['toDate']) 

        year = fromDate.year
        month = fromDate.month 

        start = fromDate.day
        end =  toDate.day
    
    for day in range(start,end + 1):
        labels.append(day)
        order = Order.objects.filter(created_at=date.today().replace(day=day).replace(year=year).replace(month=month))

        for item in order:
            order_total+=item.total_price

        if len(order) == 0:
            ordered.append(0)
            
        else:
            ordered.append(len(order))
            period_order+=len(order)
         

        print("Per order is ", period_order)    

        deliver = Order.objects.filter(status='Delivered').filter(created_at=date.today().replace(day=day).replace(year=year).replace(month=month)) 


        for item in deliver:
            deliver_total+=item.total_price

        if len(deliver) == 0:
            delivered.append(0)

        else:
            delivered.append(len(deliver))        

        returnOrders = Order.objects.filter(status='Returned').filter(created_at=date.today().replace(day=day).replace(year=year).replace(month=month))      

        for item in returnOrders:
            return_total+=item.total_price

        if len(returnOrders) == 0:
            returned.append(0)
        else:
            returned.append(len(returnOrders))

        cancel = Order.objects.filter(status='Cancelled').filter(created_at=date.today().replace(day=day).replace(year=year).replace(month=month))

        for item in cancel:
            cancel_total+=item.total_price

        if len(cancel) == 0:
            cancelled.append(0)

        else:
            cancelled.append(len(cancel))    

        piedata = [order_total,deliver_total,return_total,cancel_total]

        print("Pie", piedata)

        if deliver_total == 0:
            total_revenue = 0
        else:
            total_revenue = deliver_total - return_total


        delivered_today = Order.objects.filter(status='Delivered').filter(created_at=date.today()) 
        return_today = Order.objects.filter(status='Returned').filter(created_at=date.today())
        cancelled_today = Order.objects.filter(status='Cancelled').filter(created_at=date.today())

        for item in delivered_today:
            deliver_price+=item.total_price 

        
        for item in return_today:
            return_price+=item.total_price     

        today_revenue = deliver_price - return_price

    return JsonResponse({"labels": labels, "ordered": ordered,
    "delivered":delivered,"returned":returned,
    "cancelled":cancelled,"piedata":piedata,
    "today_order":today_order,"period_total":period_order,
    "total_revenue":total_revenue,"todays_revenue":today_revenue})


def sales_report(request):

    data = []

    order_price = 0
    delivered_price = 0
    cancelled_price = 0
    returned_price = 0
    order_total = 0
    deliver_total = 0
    cancelled_total = 0
    returned_total = 0
    no_of_orders = 0
    no_of_delivered = 0
    no_of_returned = 0
    no_of_cancelled = 0
    revenue = 0

    fromDate = date.today().replace(day=1)
    toDate = date.today()
    todays_date = date.today()
    fromObj = 1
    toObj = 31

    if request.method == "POST":
        fromDate = request.POST["fromDate"]
        toDate = request.POST["toDate"]

        print("From", fromDate)
        print("to", toDate)

        fromObj = fromDate[8] + fromDate[9]
        toObj = toDate[8] + toDate[9]

    for day in range(int(fromObj), int(toObj) + 1):
        print("Day", day)
        todays_date = date.today().replace(day=day)
        order = Order.objects.filter(created_at=date.today().replace(day=day))
        delivered = Order.objects.filter(
            created_at=date.today().replace(day=day)
        ).filter(status="Delivered")
        cancelled = Order.objects.filter(
            created_at=date.today().replace(day=day)
        ).filter(status="Cancelled")
        returned = Order.objects.filter(
            created_at=date.today().replace(day=day)
        ).filter(status="Returned")

        if len(order) == 0:
            order_price = 0
        else:
            for item in order:
                order_price += item.total_price
                no_of_orders += 1
            order_total += order_price

        if len(delivered) == 0:
            delivered_price = 0

        else:
            for item in delivered:
                delivered_price += item.total_price
                no_of_delivered += 1
            deliver_total += delivered_price

        if len(cancelled) == 0:
            cancelled_price = 0
        else:
            for item in cancelled:
                cancelled_price += item.total_price
                no_of_cancelled += 1
            cancelled_total += cancelled_price

            if len(returned) == 0:
                returned_price = 0
            else:
                for item in returned:
                    returned_price += item.total_price
                    no_of_returned += 1
            returned_total += returned_price

        data.append(
            (todays_date, order_price, delivered_price, cancelled_price, returned_price)
        )
        revenue = order_total - cancelled_total - returned_total

        print("Data", data)

        context = {
            "data": data,
            "order": order_total,
            "deliver": deliver_total,
            "cancel": cancelled_total,
            "return": returned_total,
            "revenue": revenue,
            "order_count": no_of_orders,
            "deliver_count": no_of_delivered,
            "return_count": no_of_returned,
            "cancel_count": no_of_cancelled,
        }

    return render(request, "owner/salesreport.html", context)


def sales_csv(request):
    path = "/salesreport"

    data = []

    list_header = []
    soup = BeautifulSoup(open(path), "html.parser")
    header = soup.find_all("table")[0].find("tr")

    for items in header:
        try:
            list_header.append(items.get_text())
        except:
            continue

    HTML_data = soup.find_all("table")[0].find_all("tr")[1:]

    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        data.append(sub_data)

    # Storing the data into Pandas
    # DataFrame
    dataFrame = pd.DataFrame(data=data, columns=list_header)

    # Converting Pandas DataFrame
    # into CSV file
    dataFrame.to_csv("SalesReport.csv")


def get_product(request):    
    if request.method == 'POST': 
        itemID = request.POST['itemID'] 
        product_attr = ProductAttribute.objects.filter(id=itemID).first().price
        product_size = ProductAttribute.objects.filter(id=itemID).first().size 
        product_color =  ProductAttribute.objects.filter(id=itemID) 

        product_attr_offer = ProductAttribute.objects.filter(id=itemID).first().price_after_offer

        print("Price offer ", product_attr_offer) 
        print("Price", product_attr)

        first_pro = ProductAttribute.objects.filter(id=itemID).first()

        return JsonResponse({'itemID':itemID,'product':product_attr,'product_offer':product_attr_offer, 'size':product_size})   


def check_price(request):
    if request.method == 'POST':
        pro_id = request.POST['id'] 

        product = ProductAttribute.objects.filter(product_id=pro_id) 

        for item in product:
            product_offer_price = item.price_after_offer 
            product_price = item.price 

        return JsonResponse({'offer_price':product_offer_price,'price':product_price}) 


def product_prices(request):
    pass


def landing_page(request):
    return render(request,'owner/pagemanager.html')