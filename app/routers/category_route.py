from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import category_crud
from app.schemas import category_schema
from app.database.db import get_db

router = APIRouter()

@router.post("/category", response_model=category_schema.Category)
def post_category(category: category_schema.CategoryCreate, db: Session = Depends(get_db)):
    return category_crud.create_category(db=db, category=category)

@router.get("/category", response_model=list[category_schema.Category])
def get_categories(db: Session = Depends(get_db)):
    categories = category_crud.get_categories(db)
    return categories

@router.get("/category/top", response_model=list[category_schema.CategorySales])
def get_top_categories(db: Session = Depends(get_db)):
    categories = category_crud.get_top_categories(db)
    return categories