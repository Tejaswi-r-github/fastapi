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

# pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
# def hash_password(password: str):
#     return pwd_context.hash(password)

# def verify_password(plain, hashed):
#     return pwd_context.verify(plain, hashed)        

# SECRET_KEY = "my_super_secret_key_123"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# @app.post("/register")
# def register(user:UserCreate,db:Session=Depends(get_db)):
#     db_user=db.query(database_models.User).filter(database_models.User.email==user.email).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     hashed_password = hash_password(user.password)

#     new_user = database_models.User(
#         username=user.username,
#         email=user.email,
#         password=hashed_password
#     )
#     db.add(new_user)
#     try:
#         db.commit()
#     except IntegrityError:
#         db.rollback()   
#         raise HTTPException(status_code=400, detail="Email or username already exists")
#     db.refresh(new_user)


#     return {"message": "User created successfully"}

# @app.post("/login")
# def login(user: UserLogin, db: Session = Depends(get_db)):

#     db_user = db.query(database_models.User).filter(
#         database_models.User.username == user.username
#     ).first()

#     if not db_user:
#         raise HTTPException(status_code=400, detail="Invalid username")

#     if not verify_password(user.password, db_user.password):
#         raise HTTPException(status_code=400, detail="Invalid password")
#     token = create_access_token(data={"sub": db_user.username}) # type: ignore

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# def get_current_user(token: str = Depends(oauth2_scheme)):

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")

#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         return username

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")


# @app.get("/protected")
# def protected_route(user: str = Depends(get_current_user)):
#     return {"message": f"Hello {user}, you are authenticated"}




@app.post('/user',response_model=ShowUserr)
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


@app.get('/user/{id}',response_model=models.ShowUserr)
def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(database_models.Userr).filter(database_models.Userr.id==id).first()
    if  not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with the id {id} is not available")
    
    return user
