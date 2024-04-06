import requests
from bs4 import BeautifulSoup
from model import Product
import json, csv, os

def parser(url: str):
    create_csv("kids.csv")
    list_product=[];
    res=requests.get(f"{url}&limit=100")
    soup = BeautifulSoup(res.text,"html.parser")
    products = soup.find_all(class_="product-layout")

    #print(products)
    for product in products:
        for link in product.find_all('a'):
            title = link.get('title')
            if title:
                print(title)
        price=product.find(class_="price-value").find("span").text
        print(price)
        list_product.append(Product(title=title, price=price));
    write_csv("kids.csv", list_product)
    make_json("kids.csv")


def create_csv(file1):
    with open(file1, mode="w", newline="") as file:
        writer=csv.writer(file);
        writer.writerow([
            "title",
            "price"
        ])

def write_csv(file1, products: list[Product]):
    with open(file1, mode="a", newline="") as file:
        writer = csv.writer(file);
        for product in products:
            writer.writerow([
                product.title,
                product.price
            ])


def make_json(file):
    with open(file, newline='', encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
        with open('output.json', 'w') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, separators=(',', ': '))



if __name__ =="__main__":
    parser(url="https://market.grsu.by/uslugi_obrazovatelno_issledovatelskogo_tsentra")