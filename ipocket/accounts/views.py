from django.shortcuts import render
from accounts.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login

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
            print("User Exist")

        else:
            print("Nope")

    return render(request,'user/signin.html')

