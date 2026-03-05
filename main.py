

from fastapi import FastAPI

from models import Product


app=FastAPI()

@app.get("/")
def greet():
    return "welcome to wcs"

products=[
    Product(id=1,name="watch",description="titan watches",price=90,quantity=4),
    Product(id=2,name="tv",description='samsung',price=23,quantity=2)
]


@app.get("/products")
def get_all_products():
    return products


@app.get('/product/{id}')
def get_product(id:int):
    for product in products:
        if product.id==id:
            return product
        
    return "product not found"

@app.post('/product')
def add_product(product:Product):
    products.append(product)
    return product
