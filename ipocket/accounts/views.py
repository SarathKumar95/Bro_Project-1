from django.shortcuts import render
from accounts.forms import *
from django.contrib import messages

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
