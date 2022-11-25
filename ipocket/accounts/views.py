from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from category.models import *
from django.http import HttpResponse,JsonResponse 
from cart.models import *
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
    context = {'product':product, 'category':category}
    print(product)
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
        if 'username' in request.session:
            email = request.session['username']
            product_id = request.POST['product_id']
            product_quantity = int(request.POST['product_qty'])
            product_check = Products.objects.get(product_id=product_id) 
            print("Product name is ", product_check)
            print("Stock is", product_check.quantity)
            print("Ordered qty is",product_quantity)

            if(product_check):
                    if(Cart.objects.filter(user=email,product_id=product_id)):
                        return JsonResponse({'status':"product already in cart"})         

                    else:  
                         if product_check.quantity >= product_quantity:
                            Cart.objects.create(user=email,product_id=product_id,product_qty=product_quantity)
                            return JsonResponse({'status':'Product added succesfully'})

                         else:
                            return JsonResponse({'Status':'Only' + str(product_check.quantity) + 'quantity is available.'})       
            else:
                return JsonResponse({'status':"No such product found"})    

        else:
            return JsonResponse({'STATUS': "Login to continue"})    
            
    return redirect('/')    
