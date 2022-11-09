from django.shortcuts import render,redirect
from django.http import HttpResponse
from category.models import *
from category.forms import *
from django.contrib import messages 


# Create your views here.

def product_manager(request):
    items = Products.objects.all()
    context = {'items': items}
    return render(request,'owner/productmanager.html',context)


def product_edit(request,product_id):
    item = Products.objects.get(product_id=product_id)
    print(item)
    form = ProductForm(instance=item)
    context = {'form':form}

    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=item)

        if form.is_valid:
            form.save()
            print("Saved")
            return redirect('productmanager')

        else:
            messages.error(request,form.errors)
            print("Nope!")
    return render(request,'owner/producteditor.html',context)