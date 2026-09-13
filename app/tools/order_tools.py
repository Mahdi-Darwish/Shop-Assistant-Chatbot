from app.database import SessionLocal
from app.services.order_services import get_order_by_id, get_order
def tool_get_order_status(user_id: int, order_id: int):
    db = SessionLocal()
    try:
        order = get_order_by_id(db, user_id=user_id, order_id=order_id)
        if not order:
            return {"error": "Order not found."}
        return {
            "order_id": order.id,
            "status": order.status,
            "total_price": order.total_price,
        }
    finally:
        db.close()


def tool_get_user_orders(user_id: int):
    db = SessionLocal()
    try:
        orders = get_order(db, user_id=user_id)
        return [
            {
                "order_id": o.id,
                "status": o.status,
                "total_price": o.total_price,
                "created_at": str(o.created_at),
            }
            for o in orders
        ]
    finally:
        db.close()