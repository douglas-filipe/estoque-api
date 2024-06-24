from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.crud import product_crud, category_crud
from app.schemas import product_schema
from app.database.db import get_db
from typing import List, Optional

router = APIRouter()

@router.post("/product", response_model=product_schema.Product)
def post_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    db_category = category_crud.get_category_by_id(db, id=product.category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return product_crud.create_product(db=db, product=product)

@router.get("/product", response_model=list[product_schema.ProductList])
def get_products(
    categories: Optional[List[int]] = Query(None),
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    products = product_crud.get_products(db, categories=categories, description=description)
    return products