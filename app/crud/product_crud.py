from sqlalchemy.orm import Session

from ..models.product_model import Product

from ..schemas.product_schema import ProductCreate

import requests

def create_product(db: Session, product: ProductCreate):    
    db_product = Product(
            description=product.description, 
            price=product.price, 
            category_id=product.category_id, 
            stock_quantity=product.stock_quantity,
            user_id=product.user_id,
        )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, categories: list[int] = None, description: str = None):
    query = db.query(Product).filter(Product.stock_quantity > 0)

    if categories:
        query = query.filter(Product.category_id.in_(categories))

    if description:
        query = query.filter(Product.description.like(f"%{description}%"))

    products = query.all()

    exchange_rate = get_exchange_rate()
    
    if exchange_rate is None:
        for product in products:
            product.price_in_usd = None 
    else:
        for product in products:
            product.price_in_usd = round(product.price * exchange_rate, 2)

    return products

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id==product_id).first()

def get_product_quantity(db: Session, product_id: int, quantity: int):
    product_find = db.query(Product).filter(Product.id==product_id).first()
    print('stock', product_find.stock_quantity)
    print('quantity ', quantity)
    if quantity > product_find.stock_quantity:
        return None
    else:
        return product_find
    
def update_product_quantity(db: Session, product_id: int, quantity: int):
    product = db.query(Product).filter(Product.id==product_id).first()
    product_find = db.query(Product).filter(Product.id==product_id).first()
    product_find.stock_quantity -= quantity
    db.commit() 
    db.refresh(product)  
    return product
    
def get_exchange_rate():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/BRL")
        response.raise_for_status() 
        data = response.json()
        return data["rates"]["USD"]
    except requests.exceptions.RequestException as e:
        return None
    except KeyError as e:
        return None