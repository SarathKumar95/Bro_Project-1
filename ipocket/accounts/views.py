from django.shortcuts import render, redirect
from .forms import *
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
            messages.info(request, "You are registered!")
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

        if user is not None:
            request.session['username'] = email
            return redirect('userhome')

        else:
            messages.error(request, 'Check credentials or the user may not exist.')

    return render(request, 'user/signin.html')


def signout(request):
    if 'username' in request.session:
        del request.session['username']
        return redirect('signin')


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
            print('invalid')

    return render(request, 'owner/ownin.html')


def dashboard(request):
    if 'admin' in request.session:
        return render(request, 'owner/dashboard.html')

    else:
        return redirect('owner')

def owner_out(request):
    del request.session['admin']
    return redirect('owner')
