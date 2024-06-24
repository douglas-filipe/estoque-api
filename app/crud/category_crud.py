from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.category_model import Category
from ..schemas.category_schema import CategoryCreate
from ..models.category_model import Category
from ..models.product_model import Product
from ..models.purchase_model import Purchase

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session):
    return db.query(Category).all()

def get_category_by_id(db: Session, id: str):
    return db.query(Category).filter(Category.id == id).first()


def get_top_categories(db: Session, limit: int = 3):
    # Query para obter as top categorias
    top_categories_query = (
        db.query(
            Category.id,
            Category.description,
            func.count(Purchase.id).label('sales_count')
        )
        .join(Product, Category.id == Product.category_id)
        .join(Purchase, Product.id == Purchase.product_id)
        .group_by(Category.id, Category.description)
        .order_by(func.count(Purchase.id).desc())
        .limit(limit)
        .all()
    )
    
    # Lista das top categorias
    top_categories = [
        {
            "category": {"id": category.id, "description": category.description},
            "sales_count": category.sales_count
        }
        for category in top_categories_query
    ]
    
    top_category_ids = [category["category"]["id"] for category in top_categories]

    if len(top_category_ids) > 2:
    
        other_categories_query = (
            db.query(
                Category.id,
                func.count(Purchase.id).label('sales_count')
            )
            .join(Product, Category.id == Product.category_id)
            .join(Purchase, Product.id == Purchase.product_id)
            .filter(Category.id.notin_(top_category_ids))  
            .group_by(Category.id) 
            .all()
        )
        
                
        other_categories = [
            {
                "category": {"id": None, "description": category.id},
                "sales_count": category.sales_count
            }
            for category in other_categories_query
        ]
        
        soma_sales_count = 0
        
        for item in other_categories:
            soma_sales_count += item['sales_count']
            
        others = {
            "category": {"id": 0, "description": "Outros"},
            "sales_count": soma_sales_count
        }

    else:
        others = {}
    
    combined_categories = top_categories.copy()
    
    if others:
        combined_categories.append(others)
        
    return combined_categories