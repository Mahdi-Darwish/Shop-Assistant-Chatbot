from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.product_model import Product
from sqlalchemy.exc import IntegrityError
from app.services.image_services import delete_local_image

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

def _cleanup_image(db: Session, image_url: str | None) -> None:
    """Delete an uploaded file from disk, but only if no product still uses it."""
    if not image_url:
        return
    still_used = db.scalars(select(Product).where(Product.image_url == image_url)).first()
    if not still_used:
        delete_local_image(image_url)

def create_product(db:Session,name:str,description:str,price:float,image_url:str|None=None) ->Product:
    product = Product(name=name,description=description,price=price,image_url=image_url)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db:Session,product_id:int,name:str|None = None,description:str |None = None,price:float |None = None,image_url:str|None = None ) ->Product | None:
    product = get_product_by_id(db,product_id)
    if not product:
        return None
    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if price is not None:
        product.price = price
    old_image = None
    if image_url is not None and image_url != product.image_url:
        old_image = product.image_url
        product.image_url = image_url
    db.commit()
    db.refresh(product)
    _cleanup_image(db, old_image)
    return product

def delete_product(db: Session, product_id: int) -> tuple[bool, str]:
    product = get_product_by_id(db, product_id)
    if not product:
        return False, "Product not found."
    image_url = product.image_url
    try:
        db.delete(product)
        db.commit()
        _cleanup_image(db, image_url)
        return True, "Product deleted."
    except IntegrityError:
        db.rollback()
        return False, "This product is part of an existing order or cart and cannot be deleted."
    




