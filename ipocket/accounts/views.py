from django.shortcuts import render, redirect
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
            login(request,user)
            return redirect('https://www.youtube.com/watch?v=7W58mD6sAhg')

        else:
            messages.error(request,'Check credentials or the user may not exist.')

    return render(request,'user/signin.html')

