import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

from .models import Item

def scrape_data(request):
    url = 'https://baraholka.onliner.by/viewforum.php?f=210'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    for product_div in soup.find_all("div", {"class": "x-product-view"}):
        name = product_div.find("a").text.strip()
        price_div = product_div.find("td", {"class": "cost"})
        if price_div:
            price = price_div.find("div", {"class": "price-primary"}).text.strip()
        else:
            price = "N/A"

        Item.objects.create(name=name, price=price)

    return render(request, 'myapp/items.html', {'items': Item.objects.all()})