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
    category = Categories.objects.all()
    subcat = ProductType.objects.all()
    product = Products.objects.all()
    context = {"product": product, "category": category, "subcat": subcat}
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
                   'from_date':from_date,
                   'to_date':to_date,
                   }
        
        return render(request, "owner/dashboard.html",context)
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

    if request.method == "POST":

        # range =

        if "rangeprice" in request.POST:
            print("Range is", request.POST["rangeprice"])

        else:
            pass

        if "condition" in request.POST and "productType" not in request.POST:
            condition_in = request.POST["condition"]
        

            id_of_condition = (
                Categories.objects.filter(condition=condition_in).first().category_id
            )

            

            product = Products.objects.filter(condition=id_of_condition)
            messages.success(request, "Listing " + condition_in + " products")

        elif "productType" in request.POST and "condition" not in request.POST:
            protype = request.POST["productType"]

            print("Product Type is", protype)

            id_of_protype = (
                ProductType.objects.filter(product_type=protype).first().sub_cat_id
            )

            print("Product Type id is", id_of_protype)

            product = Products.objects.filter(product_type=id_of_protype)

            messages.success(request, "Listing " + protype)

        elif "condition" and "productType" not in request.POST:
            messages.error(request, "Please select one condition and product type!")

        else:
            condition = request.POST["condition"]
            protype = request.POST["productType"]


            category_selected = Categories.objects.filter(condition=condition)
            subcategory = ProductType.objects.filter(product_type=protype)

            no_of_category = Categories.objects.filter(condition=condition).count()
            no_of_subcategory = ProductType.objects.filter(product_type=protype).count()

    
            if no_of_subcategory == 0:
                return redirect(request.path)

            else:
                for item in category_selected:
                    Cat_id = item.category_id

                for item in subcategory:
                    SubCat_id = item.sub_cat_id


                product = Products.objects.filter(
                    condition=Cat_id, product_type=SubCat_id
                )


    context = {"product": product, "category": category, "subCategory": subCategory}
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
    products = Products.objects.all()
    context = {"product": product, "products": products}
    return render(request, "home/shop-single.html", context)


# Cart functions here


def cart_add(request):

    if request.method == "POST":
        if "username" not in request.session:
            prod_id = request.POST["product_id"]
            prod_qty = 1
            product = Products.objects.filter(product_id=prod_id).first()


            cart = Cart.objects.filter(session_id=guest(request))

            for item in cart:
                cart_product_ID = item.product.product_id

            # if same product in cart
            if Cart.objects.filter(session_id=guest(request), product_id=prod_id):
                return JsonResponse(
                    {
                        "status": "Product already in cart, Please increase the quantity from cart"
                    }
                )

            else:
                cart = Cart.objects.create(
                    session_id=guest(request), product_id=prod_id, product_qty=prod_qty
                )

                return JsonResponse({"status": "Product added succesfully"})

        elif "username" in request.session:
            email = request.session["username"]
            product_id = request.POST["product_id"]
            product_quantity = 1
            product_check = Products.objects.get(product_id=product_id)
            
            if product_check:
                if Cart.objects.filter(user=email, product_id=product_id):
                    return JsonResponse({"status": "Product already in cart"})

                else:
                    if product_check.quantity >= product_quantity:
                        Cart.objects.create(
                            user=email,
                            product_id=product_id,
                            product_qty=product_quantity,
                        )
                        return JsonResponse({"status": "Product added succesfully"})

                    else:
                        return JsonResponse(
                            {
                                "status": "Only "
                                + str(product_check.quantity)
                                + " quantity is available."
                            }
                        )
            else:
                return JsonResponse({"status": "No such product found"})

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
                if Cart.objects.filter(user=user_in, product=item.product):
                    cart = Cart.objects.filter(
                        user=user_in, product=item.product
                    ).first()  # itterate and get the product

                    cart.product_qty += 1  # increase its quantity
                    cart.save()


                    # item.product.delete() # delete that product from guest cart

                else:
                    cart = Cart.objects.create(
                        user=user_in, product=item.product, product_qty=item.product_qty
                    )
                    cart.save()

            cart = Cart.objects.filter(user=user_in)

            guest_cart.delete()


    sub_total = 0

    tax = 0
    for item in cart:
        product_qtyCheck = item.product.quantity

        if item.product.price_after_offer > 0:
            Item_total = item.product.price_after_offer * item.product_qty
        else:
            Item_total = item.product.price * item.product_qty

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
        product_id = request.POST["product_id"]
        product_qty = request.POST["cart_qty"]
        cart_id = request.POST["cart_id"]

        product = Products.objects.filter(product_id=product_id)

        if "username" not in request.session:
            user_in = guest(request)
            cart = Cart.objects.filter(session_id=user_in, product=product_id).first()

        else:
            user_in = request.session["username"]
            cart = Cart.objects.filter(user=user_in, product=product_id).first()

        CartTotal = Cart.objects.filter(user=user_in)

        total = 0

        for item in CartTotal:
            if item.product.price_after_offer > 0:
                itemPrice = item.product.price_after_offer
            else:
                itemPrice = item.product.price


            total = total + itemPrice

        if cart.product.price_after_offer > 0:
            cartPrice = cart.product.price_after_offer
        else:
            cartPrice = cart.product.price

        on_change_price = total - cartPrice  # minus the existing cart price from total

        update_price = on_change_price + (cartPrice * float(product_qty))


        cart.product_qty = product_qty
        cart.save()

        return JsonResponse({"status": "Updated cart!", "update_price": update_price})

    return redirect("/")


def cart_delete(request):
    if request.method == "POST":
        prod_id = int(request.POST["product_id"])

        if "username" not in request.session:
            cart_item = Cart.objects.filter(
                session_id=guest(request), product_id=prod_id
            )
            cart_item.delete()
        else:
            user_in = request.session["username"]
            cart_item = Cart.objects.filter(user=user_in, product_id=prod_id)
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
    orders = Order.objects.all().order_by("created_at")
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
            if item.product.price_after_offer:
                price = item.product.price_after_offer
            else:
                price = item.product.price
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

                        if item.product.price_after_offer:
                            price = item.product.price_after_offer
                        else:
                            price = item.product.price

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
    print("Hit post coupon delete")
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
    
    
    userID = MyUser.objects.filter(email = request.session["username"]).first().id 

    customer_billAddress = BillingAddress.objects.filter(user_id=userID).first() 
    customer_shipAddress = ShippingAddress.objects.filter(user_id=userID).first()


    if customer_billAddress == ' ' or customer_billAddress == ' ' :
        customer_billAddress = None

    else:
        pass


    if customer_shipAddress == None or customer_shipAddress == ' ':
        customer_shipAddress = None     

    else:
        pass

    sub_total = 0
    coupon_name = None  
    total_discount = 0

    for item in cart:
        coupon_name = item.coupon_applied
        if item.product.price_after_offer > 0:
            Item_total = item.product.price_after_offer * item.product_qty
        else:
            Item_total = item.product.price * item.product_qty
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
                billAddress.addressline = request.POST['billaddressline'] 
                billAddress.city = request.POST['state']
                billAddress.state = request.POST['city']
                billAddress.pincode = request.POST['zip']    
                billAddress.save()


            elif request.POST['billaddressline'] == customer_billAddress.addressline:
                pass        
        
                if request.POST.get('save-info',True):
                    shipAddress = ShippingAddress()
                    shipAddress.user_id=userID
                    shipAddress.addressline = request.POST['shipaddressline']
                    shipAddress.city = request.POST['ship-city']
                    shipAddress.state = request.POST['ship-state']
                    shipAddress.pincode = request.POST['ship-zip']    
                    shipAddress.save()
                    print("Shipping address saved!")

                else:
                    print("Which save??")
                    

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
                if item.product.price_after_offer:
                    price = item.product.price_after_offer

                else:
                    price = item.product.price

                OrderItem.objects.create(
                    order=neworder,
                    product=item.product,
                    price=price,
                    quantity=item.product_qty,
                )

                orderproduct = Products.objects.filter(
                    product_id=item.product.product_id
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
        "customer_billAddress":customer_billAddress,
        "customer_shipAddress":customer_shipAddress,
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
    
    todays_date = date.today() 
    current_year = todays_date.year 
    current_month = todays_date.month 
    last_day_of_month = calendar.monthrange(current_year,current_month)[1] 
    
    day_order_count = [] 
    day_delivered_count = []
    day_return_count = []
    day_cancel_count = []

    period_total = 0

    #pie 

    monthly_amount = 0 
    monthly_delivered_amount = 0
    monthly_cancelled_amount = 0
    monthly_returned_amount = 0 

    # todays calcualtion 



    todays_order= len(Order.objects.filter(created_at=todays_date)) 
    todays_order_delivered= len(Order.objects.filter(created_at=todays_date).filter(status='Delivered'))    
    
    if todays_order_delivered == 0:
        todays_order_revenue = 0
    else:
        today_delivered_price = Order.objects.filter(created_at=todays_date).filter(status='Delivered').first().total_price 
        todays_order_returned_price = Order.objects.filter(created_at=todays_date).filter(status='Returned').first().total_price 
        todays_order_cancelled_price = Order.objects.filter(created_at=todays_date).filter(status='Cancelled').first().total_price
        todays_order_revenue =  today_delivered_price - todays_order_cancelled_price - todays_order_returned_price 

    for days in range(1,32):
        labels.append(days)

    for day in range(1,last_day_of_month+1):
        count_order = len(Order.objects.filter(created_at=todays_date.replace(day=day))) 
        delivered_count = len(Order.objects.filter(created_at=todays_date.replace(day=day)).filter(status='Delivered'))
        returned_count = len(Order.objects.filter(created_at=todays_date.replace(day=day)).filter(status='Returned'))
        cancelled_count = len(Order.objects.filter(created_at=todays_date.replace(day=day)).filter(status='Cancelled'))
        order= Order.objects.filter(created_at=todays_date.replace(day=day))
        delivered = Order.objects.filter(created_at=todays_date.replace(day=day)).filter(status='Delivered')
        cancelled = Order.objects.filter(created_at=todays_date.replace(day=day)).filter(status='Cancelled')
        returned = Order.objects.filter(created_at=todays_date.replace(day=day)).filter(status='Returned')
        day_order_count.append(count_order)
        day_delivered_count.append(delivered_count)
        day_return_count.append(returned_count)
        day_cancel_count.append(cancelled_count) 
        


        if len(order) == 0:
            pass

        else:
            for item in order:
                monthly_amount+=item.total_price 
                if item != 0:
                    period_total+=1
        
        
        if len(delivered) == 0:
            pass

        else:
            for item in delivered:
                monthly_delivered_amount+=item.total_price    
    

                
        if len(returned) == 0:
            pass

        else:
            for item in returned:
                monthly_returned_amount+=item.total_price    

                    
        if len(cancelled) == 0:
            pass

        else:
            for item in returned:
                monthly_cancelled_amount+=item.total_price  
                  
    
    less_cancelled = monthly_delivered_amount - monthly_cancelled_amount - monthly_returned_amount
    
    total_revenue = less_cancelled 

    
    if request.method == 'POST':
        from_Date = parse_date(request.POST.get('fromDate'))
        to_Date = parse_date(request.POST.get('toDate')) 

        
        day_order_count.clear() 
        day_delivered_count.clear()
        day_return_count.clear()
        day_cancel_count.clear()
        labels.clear() 


        
        #pie 

        monthly_amount = 0 
        monthly_delivered_amount = 0
        monthly_cancelled_amount = 0
        monthly_returned_amount = 0
        period_total = 0
        
        for days in range(from_Date.day,to_Date.day + 1):
            labels.append(days)


        print("Labels is ",labels)    

        
        for day in range(from_Date.day,to_Date.day+1):
            count_order = len(Order.objects.filter(created_at=todays_date.replace(day=day))) 
            delivered_count = len(Order.objects.filter(created_at=todays_date.replace(day=day)).filter(status='Delivered'))
            returned_count = len(Order.objects.filter(created_at=todays_date.replace(day=day)).filter(status='Returned'))
            cancelled_count = len(Order.objects.filter(created_at=todays_date.replace(day=day)).filter(status='Cancelled'))
            order= Order.objects.filter(created_at=todays_date.replace(day=day))
            delivered = Order.objects.filter(created_at=todays_date.replace(day=day)).filter(status='Delivered')
            cancelled = Order.objects.filter(created_at=todays_date.replace(day=day)).filter(status='Cancelled')
            returned = Order.objects.filter(created_at=todays_date.replace(day=day)).filter(status='Returned')
            day_order_count.append(count_order)
            day_delivered_count.append(delivered_count)
            day_return_count.append(returned_count)
            day_cancel_count.append(cancelled_count) 

            
            if len(order) == 0:
                pass

            else:
                for item in order:
                    monthly_amount+=item.total_price 
                    if item != 0:
                        period_total +=1

            if len(delivered) == 0:
                pass

            else:
                for item in delivered:
                    monthly_delivered_amount+=item.total_price    
                    

                
            if len(returned) == 0:
                pass

            else:
                for item in returned:
                    monthly_returned_amount+=item.total_price    

                    
            if len(cancelled) == 0:
                pass

            else:
                for item in returned:
                    monthly_cancelled_amount+=item.total_price    

        less_cancelled = monthly_delivered_amount - monthly_cancelled_amount - monthly_returned_amount
    
        total_revenue = less_cancelled    

    
    piedata = [monthly_amount,monthly_delivered_amount,monthly_returned_amount,monthly_cancelled_amount] 


    return JsonResponse(data={
        'labels':labels,
        'ordered' : day_order_count,
        'delivered' : day_delivered_count,
        'returned' : day_return_count,
        'cancelled':day_cancel_count,
        'total_revenue' : total_revenue,
        'today_order':todays_order,
        'period_total':period_total,
        'todays_revenue':todays_order_revenue,
        'piedata':piedata           
        
    })    

    
