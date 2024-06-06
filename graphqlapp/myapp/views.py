import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

from .models import Item

def scrape_data(request):
    url = 'https://baraholka.onliner.by/viewforum.php?f=210'
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"lxml")
    for item in soup.select('.ba-tbl-list__table'):
        name_element = item.select_one('.txt a')
        if name_element:
            name = name_element.text.strip()
        else:
            name = 'N/A'

        price_element = item.select_one('.cost .price-primary')
        if price_element:
            price = price_element.text.strip()
        else:
            price = 'N/A'

        Item.objects.create(name=name, price=price)

    return render(request, 'myapp/items.html', {'items': Item.objects.all()})