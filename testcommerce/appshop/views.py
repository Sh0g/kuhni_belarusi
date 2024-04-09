from django.shortcuts import render
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
