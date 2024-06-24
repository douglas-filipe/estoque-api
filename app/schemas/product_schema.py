from pydantic import BaseModel
from typing import Optional

from app.schemas.category_schema import Category
from app.schemas.user_schema import UserOut

class ProductBase(BaseModel):
    description: str
    price: float 
    category_id: int
    stock_quantity: int
    user_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    category: Optional[Category] = None 
    user: Optional[UserOut] = None

    class Config:
        orm_mode = True

class ProductList(Product):
    id: int
    description: str
    price: float 
    category_id: int
    stock_quantity: int
    user_id: int
    price_in_usd: Optional[float]

    class Config:
        orm_mode = True