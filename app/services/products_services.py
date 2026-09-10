from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.product_model import Product
from sqlalchemy.exc import IntegrityError

def get_products(db:Session) ->list[Product]:
    statement = (select(Product))
    return db.scalars(statement).all() 

def search_product_by_name(db:Session,name:str) ->list[Product]:
    statement = (select(Product).where(Product.name.ilike(f"%{name}%")))
    return db.scalars(statement).all()

def get_products_by_min_price(db:Session,min_price:float) ->list[Product]:
    statement = (select(Product).where(Product.price >= min_price).order_by(Product.price.asc()))
    return db.scalars(statement).all()

def get_products_by_max_price(db:Session,max_price:float) ->list[Product]:
    statement = (select(Product).where(Product.price <= max_price).order_by(Product.price.asc()))
    return db.scalars(statement).all()

def get_product_by_id(db:Session,product_id:int) -> Product | None:
    statement = select(Product).where(Product.id==product_id)
    return db.scalars(statement).first()

def create_product(db:Session,name:str,description:str,price:float) ->Product:
    product = Product(name=name,description=description,price=price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db:Session,product_id:int,name:str|None = None,description:str |None = None,price:float |None = None ) ->Product | None:
    product = get_product_by_id(db,product_id)
    if not product:
        return None
    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if price is not None:
        product.price = price
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> tuple[bool, str]:
    product = get_product_by_id(db, product_id)
    if not product:
        return False, "Product not found."
    try:
        db.delete(product)
        db.commit()
        return True, "Product deleted."
    except IntegrityError:
        db.rollback()
        return False, "This product is part of an existing order or cart and cannot be deleted."
    


    

