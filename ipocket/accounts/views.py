from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from category.models import *
from django.http import HttpResponse 

# Create your views here.

def home_page(request):
    #category = Category.objects.all()
    product = Products.objects.all()
    context = {'product':product}
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

    if 'username' in request.session:
        return redirect('userhome')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        print(user)
        if user is not None and user.is_active == True:
            request.session['username'] = email
            return redirect('home')

        else:
            messages.error(request, 'Check credentials or contact admin.')

    return render(request, 'user/signin.html')


def signout(request):
    if 'username' in request.session:
        del request.session['username']
        return redirect('/')   


def myaccount(request):
    if 'username' in request.session:
        return render(request, 'user/userhome.html')
    return redirect('signin')


def owner(request):
    if 'admin' in request.session:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('adminuser')
        password = request.POST.get('adminpass')

        admin = authenticate(username=username, password=password)

        if admin is not None:
            request.session['admin'] = username
            return redirect('dashboard')

        else:
            messages.error(request,"Fatal! You don't seem to be an admin")

    return render(request, 'owner/signin.html')


def dashboard(request):
    if 'admin' in request.session:
        return render(request, 'owner/dashboard.html')

    else:
        return redirect('owner')

def owner_out(request):
    del request.session['admin']
    messages.info(request,"Thank you for spending time with us.")
    return redirect('owner')


def user_manager(request):
    if 'admin' in request.session:
        users = MyUser.objects.all()
        no_of_users = MyUser.objects.filter().count()
        no_of_superuser = MyUser.objects.filter(is_superuser=True).count()
        no_of_filtered_users = no_of_users - no_of_superuser
        # print("No of users to the front end is : ", no_of_filtered_users)
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
    category = Category.objects.all() 
    context = {'product':product, 'category':category}
    print(product)
    return render(request,'home/shop.html',context)


def item(request,product_id):
    product = Products.objects.filter(product_id=product_id)
    products = Products.objects.all()
    context = {'product':product,'products':products}
    
    if request.method == 'POST':
        quantity = request.POST.get('product-quantity')
        user_in = request.session.get('username')
        return HttpResponse(quantity)
    
    return render(request,'home/shop-single.html',context)


def signin_Otp(request):
    pass