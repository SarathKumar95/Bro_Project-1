from django.shortcuts import render, redirect
from django.http import HttpResponse
from category.models import *
from category.forms import *
from django.contrib import messages


# Create your views here.


def product_manager(request):
    products = Products.objects.all()
    form = ProductForm()
    context = {'products': products, 'form':form}
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
            messages.success(request,"Product Updated!")
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


def list_categories(request):
    category = Categories.objects.all()
    form = CategoryForm()
    context = {'category':category,'form':form}
    
    if request.method == 'POST':
        form = CategoryForm(request.POST) 

        if form.is_valid():
            form.save() 
            messages.info(request, "Category added")
        else:
            messages.error(request,form.error)    
    return render(request,'owner/categorylist.html',context)


def producttype_list(request):
    product_type = ProductType.objects.all() 
    form = ProductTypeForm()
    context = {'product_type': product_type, 'form':form} 

    if request.method == 'POST':
        form = ProductTypeForm(request.POST,request.FILES) 

        if form.is_valid():
            form.save()
            messages.info(request, "Product Type Added")

        else:
            messages.error(request,form.errors)
    return render(request,'owner/producttypelist.html',context)

def producttype_delete(request,sub_cat_id):
    product_type = ProductType.objects.get(sub_cat_id=sub_cat_id) 
    product_type.delete()
    messages.success(request,"Deleted Product Type")
    return redirect('product-type-list')


def producttype_edit(request,sub_cat_id):
    product_type = ProductType.objects.get(sub_cat_id=sub_cat_id) 
    form = ProductTypeForm(instance=product_type) 
    context = {'product_type':product_type, 'form':form}
    
    if request.method == 'POST':
        form = ProductTypeForm(request.POST,request.FILES,instance=product_type)

        if form.is_valid():
            form.save() 
            messages.success(request,"Product Type Updated")
            return redirect('product-type-list')

        else:
            messages.error(request,form.errors) 

    return render(request,'owner/producttypeedit.html',context)        


def edit_categories(request,category_id):
    category = Categories.objects.get(category_id=category_id) 
    form = CategoryForm(instance=category) 
    context = {'form':form}
    
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)

        if form.is_valid():
            form.save() 
            messages.success(request,"Category Updated") 
            return redirect('category-list')
        else:
            messages.error(request,form.errors) 
    return render(request,'owner/categoryedit.html',context)           


def delete_categories(request,category_id):
    category = Categories.objects.get(category_id=category_id) 
    category.delete()
    messages.success(request,"Deleted Category") 

    return redirect('category-list') 


def cart_list(request):
    return render(request,'home/cartlist.html')    