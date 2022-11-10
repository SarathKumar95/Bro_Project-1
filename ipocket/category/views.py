from django.shortcuts import render, redirect
from django.http import HttpResponse
from category.models import *
from category.forms import *
from django.contrib import messages


# Create your views here.

def product_manager(request):
    items = Products.objects.all()
    context = {'items': items}
    return render(request, 'owner/productmanager.html', context)

def product_edit(request,product_id):
    item = Products.objects.get(product_id=product_id)
    print(item)
    form = ProductForm(instance=item)
    context = {'form':form}

    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=item)

        if form.is_valid():
            form.save()
            print("Saved")
            return redirect('productmanager')

        else:
            messages.error(request,form.errors)
            print("Nope!")
    return render(request,'owner/producteditor.html',context)


def product_add (request):
    form = ProductForm()
    context = {'form':form}
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES) 
        
        if form.is_valid():
            form.save()
            messages.info(request,'Product added')
        return redirect('productmanager')

    else:
        print(form.errors)    
    return render(request,'owner/addproducts.html',context)

def delete_product(request,product_id):
    product = Products.objects.get(product_id=product_id)
    product.delete()
    messages.info(request, "Product Deleted")
    return redirect('productmanager')


def category_list(request):
    items = Categories.objects.all()
    context = {'items':items}
    return render(request,'owner/categorymanager.html',context)


def category_add(request):    

    form = CategoryForm()
    context = {'form':form}

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Category Added!")
        else:
            messages.error(request,form.errors)
            return redirect("categorymanager")    
    return render(request,'owner/categoryadd.html',context)




def category_delete(request,category_id):
    category = Categories.objects.get(category_id=category_id)
    category.delete()
    name_of_cat = category.category_name
    messages.info(request,"Deleted " + str(name_of_cat))
    return redirect('categorymanager')





def category_edit(request,category_id):
    category = Categories.objects.get(category_id=category_id)
    form = CategoryForm(instance=category)
    context = {'category':category, 'form':form}

    if request.method == "POST":
        form = CategoryForm(request.POST,instance=category)

        if form.is_valid():
            form.save()
            messages.info(request,"Category updated.")
            return redirect("categorymanager")

    return render(request,'owner/categoryedit.html',context)    