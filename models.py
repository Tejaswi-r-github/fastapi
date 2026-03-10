from pydantic import BaseModel,EmailStr


class Product(BaseModel):
    id:int
    name:str
    description:str
    price:float
    quantity:int


class Userr(BaseModel):
    name:str
    email:str
    password:str


class ShowUserr(BaseModel):
    name:str
    email:str
    class config():
        orm_mode=True