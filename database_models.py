from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Product(Base):
    __tablename__="product"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100))
    description=Column(String(200))
    price=Column(Integer)
    quantity=Column(Integer)

class Userr(Base):
    __tablename__ = "userr"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email=Column(String,unique=True,index=True)
    password = Column(String)