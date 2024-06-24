from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from ..models.purchase_model import Purchase
from ..models.product_model import Product
from sqlalchemy import func

from ..schemas.purchase_schema import PurchaseCreate

def create_purchase(db: Session, purchase: PurchaseCreate):    
    db_purchase = Purchase(
        product_id=purchase.product_id,
        user_id=purchase.user_id,
        quantity=purchase.quantity,
        purchase_date=datetime.now()
    )
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

def get_purchases(db: Session):
    return db.query(Purchase).all()

def get_last_purchases(db: Session):
    query = db.query(Purchase).order_by(desc(Purchase.purchase_date)).limit(4).all()

    return query

def get_top_selling_products(db: Session, limit: int = 10):    
    top_selling_products = (
        db.query(Product, func.sum(Purchase.quantity).label('total_quantity'))
        .join(Purchase, Purchase.product_id == Product.id)
        .group_by(Product.id)
        .order_by(func.sum(Purchase.quantity).desc())
        .limit(limit)
        .all()
    )
    
    return [
        {"product": product, "total_quantity": total_quantity} 
        for product, total_quantity in top_selling_products
    ]