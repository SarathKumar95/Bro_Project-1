from django.shortcuts import render, redirect
from accounts.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def register(request):
    form = CustomUserCreationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.info(request,"You are registered!")
        else:
            messages.error(request,form.errors)

    return render(request, 'user/register.html', context)


def signin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')


    if request.method == 'POST':
        user = authenticate(username = email, password=password)

        if user is not None:
            login(request,user)
            return redirect('userhome')

        else:
            messages.error(request,'Check credentials or the user may not exist.')

    return render(request,'user/signin.html')



def signout(request):
    logout(request)
    return redirect('signin')


def myaccount(request):
    return render(request,'user/userhome.html')

def owner(request):
    username = request.POST.get('adminuser')
    password = request.POST.get('adminpass')

    admin = authenticate(username=username,password=password)

    if admin is not None:
        return redirect('dashboard')

    else:
        messages.info(request,'You dont seem to be an admin.')

    return render(request,'owner/ownin.html')


def dashboard(request):
    return render(request,'owner/dashboard.html')


def owner_out(request):
    logout(request)
    return redirect('owner')