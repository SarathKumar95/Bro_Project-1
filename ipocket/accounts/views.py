from django.shortcuts import render
from accounts.forms import *

# Create your views here.


def register(request):
    form = CustomUserCreationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            print('Yes')
        else:
            print('Nope!')
    return render(request, 'user/register.html', context)
