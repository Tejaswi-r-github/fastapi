from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from models import Product
from database import session, engine
import database_models

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
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products


# Get single product
@app.get('/product/{id}')
def get_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if db_product:
        return db_product
    else:
        return {"message": "product not found"}


# Add product
@app.post('/product')
def add_product(product: Product, db: Session = Depends(get_db)):
    db_product = database_models.Product(**product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


# Update product
@app.put('/product')
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
@app.delete('/product')
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