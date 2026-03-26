from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base=declarative_base()



class Userr(Base):
    __tablename__ = "userr"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email=Column(String,unique=True,index=True)
    password = Column(String)
    products=relationship("Product",back_populates='owner')

class Product(Base):
    __tablename__="product"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100))
    description=Column(String(200))
    price=Column(Integer)
    quantity=Column(Integer)
    user_id=Column(Integer,ForeignKey("userr.id"))
    category=Column(String(100))
    owner=relationship('Userr',back_populates='products')


