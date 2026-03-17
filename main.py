from fastapi import Depends, FastAPI,HTTPException
from sqlalchemy.orm import Session
from datetime import datetime,timedelta
from sqlalchemy.exc import IntegrityError
from models import Product,Userr,ShowUserr
from database import session, engine
import database_models,models
from hashing import Hash
from passlib.context import CryptContext
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import status

from jose import JWTError,jwt

app = FastAPI()


# Dependency to get DB session
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# Create tables
database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "welcome to wcs"


# Initial products
products = [
    Product(id=1, name="watch", description="titan watches", price=90, quantity=4),
    Product(id=2, name="tv", description="samsung", price=23, quantity=2)
]


# Insert initial data if table empty
def init_db():
    db = session()
    count = db.query(database_models.Product).count()

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

    db.close()


init_db()


# Get all products
@app.get("/products",tags=['products'])
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products


# Get single product
@app.get('/product/{id}',tags=['products'])
def get_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if db_product:
        return db_product
    else:
        return {"message": "product not found"}


# Add product
@app.post('/product',tags=['products'])
def add_product(product: Product, db: Session = Depends(get_db)):
    db_product = database_models.Product(**product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


# Update product
@app.put('/product',tags=['products'])
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity

        db.commit()
        return {"message": "product updated successfully"}

    else:
        return {"message": "product not found"}


# Delete product
@app.delete('/product',tags=['products'])
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "product deleted"}

    else:
        return {"message": "product not found"}








@app.post('/user',response_model=ShowUserr,tags=['user'])
def create_user(userr:Userr,db: Session = Depends(get_db)):
    #new_user=database_models.Userr(**userr.model_dump())
    new_user=database_models.Userr(
        name=userr.name,
        email=userr.email,
        password=Hash.hash_password(userr.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}',response_model=models.ShowUserr,tags=['user'])
def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(database_models.Userr).filter(database_models.Userr.id==id).first()
    if  not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with the id {id} is not available")
    
    return user





from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def middleware(request,call_next):
    print("before")
    response=await call_next(request)
    print("after")
    return response

from sqlalchemy import text
@app.get('/customers')
def get_customers(db:Session=Depends(get_db)):
    data=db.execute(text("select * from customers")).fetchall()
    return [dict(row._mapping) for row in data]



@app.get('/orders')
def get_orders(db:Session=Depends(get_db)):
    data=db.execute(text("select * from orders")).fetchall()
    return [dict(row._mapping) for row in data]