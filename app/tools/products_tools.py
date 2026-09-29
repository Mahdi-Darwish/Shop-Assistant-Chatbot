from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.product_model import Product
from app.services.products_services import(get_products,search_product_by_name,get_products_by_max_price,get_products_by_min_price)

def _serialize(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        # Picked up by app/services/chat_cards.py and removed before the
        # result is shown to the LLM.
        "image_url": product.image_url,
    }

def tool_get_products():
    db = SessionLocal()
    try:
        return [_serialize(p) for p in get_products(db)]
    finally:
        db.close()

def tool_search_product_by_name(name:str):
    db = SessionLocal()
    try:
        return [_serialize(p) for p in search_product_by_name(db=db, name=name)]
    finally:
        db.close()

def tool_get_products_by_max_price (max_price:float):
    db= SessionLocal()
    try:
        return [_serialize(p) for p in get_products_by_max_price(db=db,max_price=max_price)]
    finally:
        db.close()

def tool_get_products_by_min_price (min_price:float):
    db = SessionLocal()
    try:
        return [_serialize(p) for p in get_products_by_min_price(db=db,min_price=min_price)]
    finally:
        db.close()
