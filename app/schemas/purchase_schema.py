from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.schemas.product_schema import Product 
from app.schemas.user_schema import UserOut

class PurchaseBase(BaseModel):
    product_id: int
    user_id: int
    purchase_date: datetime
    quantity: int

class PurchaseCreate(PurchaseBase):
    pass

class Purchase(PurchaseBase):
    id: int
    product: Optional[Product]
    user: Optional[UserOut]

    class Config:
        orm_mode = True
        
        
class TopSellingProduct(BaseModel):
    product: Product
    total_quantity: int

    class Config:
        orm_mode = True