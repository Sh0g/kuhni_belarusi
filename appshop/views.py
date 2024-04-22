from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Product
from rest_framework import serializers
from rest_framework import generics
from appshop.serializers import ItemSerializer

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

class ItemListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get('sort_by', 'name')
        order_by = self.request.query_params.get('order_by', 'asc')

        if sort_by == 'name':
            queryset = queryset.order_by('name' if order_by == 'asc' else '-name')
        elif sort_by == 'prices':
            queryset = queryset.order_by('prices' if order_by == 'asc' else '-prices')

        return queryset

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


def sortname(request):
    if request.method=="POST":
      data = Product.objects.order_by('name')
      template = loader.get_template('index.html')
      context = {
        'items': data,
      }
    return HttpResponse(template.render(context, request))
