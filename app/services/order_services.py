from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.order_model import Order

def get_order(db: Session, user_id: int) -> list[Order] | None:
    statement = select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
    return db.scalars(statement).all()

def get_order_by_id(db: Session, order_id: int, user_id: int) -> Order | None:
    statement = select(Order).where(Order.id == order_id, Order.user_id == user_id)
    return db.scalars(statement).first()

def get_all_orders(db: Session, status: str | None = None) -> list[Order]:
    statement = select(Order).order_by(Order.created_at.asc())
    if status:
        statement = statement.where(Order.status == status)
    return db.scalars(statement).all()


def update_order_status(db: Session, order_id: int, new_status: str) -> Order | None:
    order = db.get(Order, order_id)
    if not order:
        return None
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order