from pydantic import BaseModel

class CategoryBase(BaseModel):
    description : str

class CategoryCreate(CategoryBase):
    description: str

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True
        
class CategorySales(BaseModel):
    category: Category
    sales_count: int