from app.models.cart_model import Cart,CartItem
from app.models.order_model import Order,OrderItem
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_active_cart(db:Session,user_id:int) ->Cart | None:
    statement = select(Cart).where(Cart.user_id == user_id,Cart.status == "active")
    return db.scalars(statement).first()

def get_or_create_active_cart(db:Session,user_id:int) ->Cart:
    cart = get_active_cart(db,user_id)
    if cart:
        return cart
    cart = Cart(user_id=user_id, status="active")
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

def add_item_to_cart(db:Session,user_id:int,product_id:int,quantity:int =1) ->CartItem:
    cart = get_or_create_active_cart(db,user_id)
    statement = select(CartItem).where(CartItem.cart_id == cart.id,CartItem.product_id == product_id)
    existing_item = db.scalars(statement).first()
    if existing_item:
        existing_item.quantity += quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def remove_item_from_cart(db:Session,user_id:int,quantity:int,product_id:int | None = None) -> bool:
    cart = get_active_cart(db, user_id)
    if not cart:
        return False
    statement = select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
    item = db.scalars(statement).first()
    if not item:
        return False
    if quantity is None or item.quantity <= quantity:
        db.delete(item)
    else:
        item.quantity -= quantity
        db.commit()
        return True
    
def get_cart_with_items(db: Session, user_id: int) -> tuple[Cart, list[CartItem]] | None:
    cart = get_active_cart(db, user_id)
    if not cart:
        return None
    statement = select(CartItem).where(CartItem.cart_id == cart.id)
    items = db.scalars(statement).all()
    return cart, items
 
 
def clear_cart(db: Session, user_id: int) -> None:
    cart = get_active_cart(db, user_id)
    if not cart:
        return
    statement = select(CartItem).where(CartItem.cart_id == cart.id)
    for item in db.scalars(statement).all():
        db.delete(item)
    db.commit()
 
 
def checkout_cart(db: Session, user_id: int) -> Order | None:
    cart = get_active_cart(db, user_id)
    if not cart or not cart.items:
        return None
 
    order = Order(user_id=user_id, status="pending", total_price=0.0)
    db.add(order)
    db.flush()
 
    total = 0.0
    for item in cart.items:
        product = item.product
        line_total = product.price * item.quantity
        total += line_total
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                price_at_purchase=product.price,
            )
        )
    order.total_price = total
    cart.status = "checked_out"
    db.commit()
    db.refresh(order)
    return order