from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.models.order_model import Order, OrderItem
from app.models.user_model import User

VALID_STATUSES = (
    "pending", "preparing", "ready",
    "out_for_delivery", "delivered", "cancelled",
)
STATUS_MESSAGES = {
    "pending": "has been received and is pending",
    "preparing": "is now being prepared",
    "ready": "is ready for pickup",
    "out_for_delivery": "is on its way to you",
    "delivered": "has been delivered",
    "cancelled": "has been cancelled",
}

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


def get_orders_with_customers(db: Session, limit: int = 200) -> list:
    """Newest first, with each order's items/products and its customer loaded
    in a few queries — used by the admin dashboard's live orders board."""
    statement = (
        select(Order, User)
        .join(User, User.id == Order.user_id)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
        .order_by(Order.id.desc())
        .limit(limit)
    )
    return db.execute(statement).all()


def get_order_with_customer(db: Session, order_id: int):
    statement = (
        select(Order, User)
        .join(User, User.id == Order.user_id)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
        .where(Order.id == order_id)
    )
    return db.execute(statement).first()


def update_order_status_and_notify(
    db: Session, order_id: int, new_status: str
) -> tuple[Order | None, str | None]:
    """Shared by the admin chat tool and the dashboard buttons. Validates the
    status, saves it, and tells the customer in their chat. Returns
    (order, None) on success or (None, error_message). Setting the status an
    order already has is a no-op, so a double click can't notify twice."""
    from app.services.chat_services import (
        create_conversation,
        get_conversations_by_user,
        save_message,
    )
    if new_status not in VALID_STATUSES:
        return None, f"Status must be one of: {', '.join(VALID_STATUSES)}."
    order = db.get(Order, order_id)
    if not order:
        return None, f"No order found with id {order_id}."
    if order.status == new_status:
        return order, None
    order = update_order_status(db, order_id=order_id, new_status=new_status)
    conversations = get_conversations_by_user(db, user_id=order.user_id)
    conversation = conversations[0] if conversations else create_conversation(db, user_id=order.user_id)
    notification = f"Update: your order #{order.id} {STATUS_MESSAGES[new_status]}."
    save_message(db, conversation_id=conversation.id, role="assistant", content=notification)
    return order, None
