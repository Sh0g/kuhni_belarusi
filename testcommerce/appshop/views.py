from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product

def index (request):
    items = Product.objects.all()
    context = {
        'items':items
    }
    return render(request, "appshop/index.html", context)

def index_item(request, id):
    item = Product.objects.get(id=id)
    context = {
        'item': item
    }
    return render(request, "appshop/detail.html", context=context)

def add_item(request):
    if request.method=="POST":
        name = request.POST.get("name")
        prices = request.POST.get("prices")
        description = request.POST.get("description")
        image= request.FILES.get("upload")
        item = Product(name=name, prices=prices, description=description, image=image)
        item.save()
    return render(request, "appshop/additem.html")

def update_item(request, id):
    item = Product.objects.get(id=id)
    if request.method=="POST":
        item.name = request.POST.get("name")
        item.prices = request.POST.get("prices")
        item.description = request.POST.get("description")
        item.image= request.FILES.get("upload", item.image)
        item.save()
        redirect("/appshop/")
    context = {
        'item': item
    }
    return render(request, "appshop/update.html", context=context)

def delete_item(request, id):
    item = Product.objects.get(id=id)
    if request.method=="POST":
        item.delete()
        redirect("/appshop/")
    context = {
        'item': item
    }
    return render(request, "appshop/delete.html", context=context)
