from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.product_model import Product
from app.services.products_services import(get_products,search_product_by_name,get_products_by_max_price,get_products_by_min_price)

def tool_get_products():
    db = SessionLocal()
    try:
        products = get_products(db)
        return [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
            }
            for product in products
        ]
    finally:
        db.close()

def tool_search_product_by_name(name:str):
    db = SessionLocal()
    try:
        products = search_product_by_name(db=db, name=name)
        return [
            {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
        }
        for product in products
    ]
    finally:
         db.close()
 

def tool_get_products_by_max_price (max_price:float):
    db= SessionLocal()
    try:
         products = get_products_by_max_price(db=db,max_price=max_price)
         return [
            {
            'id':product.id,
            'name':product.name,
            'description':product.description,
            'price':product.price
        }
        for product in products
    ]
    finally:
        db.close()


def tool_get_products_by_min_price (min_price:float):
    db = SessionLocal()
    try:
       products = get_products_by_min_price(db=db,min_price=min_price)
       return [
           {
            'id':product.id,
            'name':product.name,
            'description':product.description,
            'price':product.price
         }
         for product in products
    ]
    finally:
        db.close()



