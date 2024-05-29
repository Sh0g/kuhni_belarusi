from fastapi import FastAPI, Depends
import uvicorn
from graphene import ObjectType, String, Field, Schema, List
from starlette_graphene3 import GraphQLApp
from starlette.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
import jwt
from datetime import datetime, timedelta

# FastAPI app instance
app = FastAPI()

# GraphQL app instance
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# JWT authentication setup
SECRET_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6InVzZXIiLCJpYXQiOjE3MTY4OTA0OTh9.s6Daf4E5PpMEkYc9PQz6DPdcl1928iif5jA0bDTAZmI'
ALGORITHM = "HS256"

# GraphQL schema definition
class ProductData(ObjectType):
    name = String()
    price = String()

class Query(ObjectType):
    products = List(ProductData)

    def resolve_products(self, info):
        # Fetch data from the URL
        url = "https://baraholka.onliner.by/viewforum.php?f=210"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")

        # Extract name and price from the HTML
        products = []
        for product_div in soup.find_all("div", {"class": "x-product-view"}):
            name = product_div.find("a").text.strip()
            price_div = product_div.find("td", {"class": "cost"})
            if price_div:
                price = price_div.find("div", {"class": "price-primary"}).text.strip()
            else:
                price = "N/A"
            products.append({"name": name, "price": price})

        return products

# JWT authentication middleware
async def get_current_user(token: str = Depends(None)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return {"username": username}
    except jwt.exceptions.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None

# GraphQL app with JWT authentication
schema = Schema(query=Query)
graphql_app = GraphQLApp(schema=schema, middleware=[get_current_user])

# Mount GraphQL app on the root path
app.add_route("/graphql", graphql_app)

# Generate JWT token (for testing purposes)
def generate_token(username):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)