from app.database import SessionLocal
from app.services.products_services import (create_product,delete_product,get_products,search_product_by_name,update_product,)
from app.services.user_services import (delete_user,all_users as get_all_users,search_users_by_username, set_user_active_status,)
from app.services.order_services import update_order_status
from app.services.order_services import get_all_orders
from app.services.user_services import get_user_by_id

def _resolve_single_product(db, product_name: str):
    matches = search_product_by_name(db=db, name=product_name)
    if not matches:
        return None, {"error": f"No product found matching '{product_name}'."}
    if len(matches) > 1:
        return None, {
            "error": "Multiple products match that name — ask which one they mean.",
            "matches": [{"id": p.id, "name": p.name, "price": p.price} for p in matches],
        }
    return matches[0], None
def _resolve_single_user(db, username: str):
    matches = search_users_by_username(db, username)
    if not matches:
        return None, {"error": f"No user found matching '{username}'."}
    if len(matches) > 1:
        return None, {
            "error": "Multiple users match that name — ask which one they mean.",
            "matches": [{"id": u.id, "username": u.username} for u in matches],
        }
    return matches[0], None

#tools for products
def tool_add_product(name: str, description: str, price: float):
    db = SessionLocal()
    try:
        product = create_product(db, name=name, description=description, price=price)
        return {
            "message": f"Added '{product.name}' at ${product.price:.2f}.",
            "product_id": product.id,
        }
    finally:
        db.close()
def tool_list_products():
    db = SessionLocal()
    try:
        products = get_products(db)
        return [
            {"id": p.id, "name": p.name, "description": p.description, "price": p.price}
            for p in products
        ]
    finally:
        db.close()

def tool_update_product(
    product_name: str,
    new_name: str | None = None,
    new_description: str | None = None,
    new_price: float | None = None,
):
    db = SessionLocal()
    try:
        product, error = _resolve_single_product(db, product_name)
        if error:
            return error
        updated = update_product(
            db, product_id=product.id, name=new_name, description=new_description, price=new_price
        )
        return {
            "message": f"Updated '{updated.name}'.",
            "product": {"id": updated.id, "name": updated.name, "description": updated.description, "price": updated.price},
        }
    finally:
        db.close()

def tool_remove_product(product_name: str):
    db = SessionLocal()
    try:
        product, error = _resolve_single_product(db, product_name)
        if error:
            return error
        success, message = delete_product(db, product_id=product.id)
        if not success:
            return {"error": message}
        return {"message": message}
    finally:
        db.close()

#tools for users
def tool_list_users():
    db = SessionLocal()
    try:
        users = get_all_users(db)
        return [
            {
                "id": u.id,
                "username": u.username,
                "phone": u.phone,
                "role": u.role,
                "is_active": u.is_active,
            }
            for u in users
        ]
    finally:
        db.close()
def tool_deactivate_user(admin_id: int, username: str):
    db = SessionLocal()
    try:
        user, error = _resolve_single_user(db, username)
        if error:
            return error
        if user.id == admin_id:
            return {"error": "You can't deactivate your own account through chat."}
        updated = set_user_active_status(db, user_id=user.id, is_active=False)
        return {"message": f"Deactivated '{updated.username}'."}
    finally:
        db.close()

def tool_activate_user(admin_id: int, username: str):
    db = SessionLocal()
    try:
        user, error = _resolve_single_user(db, username)
        if error:
            return error
        updated = set_user_active_status(db, user_id=user.id, is_active=True)
        return {"message": f"Reactivated '{updated.username}'."}
    finally:
        db.close()

def tool_delete_user(admin_id: int, username: str):
    db = SessionLocal()
    try:
        user, error = _resolve_single_user(db, username)
        if error:
            return error
        if user.id == admin_id:
            return {"error": "You can't delete your own account through chat."}
        success, message = delete_user(db, user_id=user.id)
        if not success:
            return {"error": message}
        return {"message": message}
    finally:
        db.close()
        
#tools for orders
def tool_list_orders(status: str | None = None):
    db = SessionLocal()
    try:
        orders = get_all_orders(db, status=status)
        result = []
        for o in orders:
            user = get_user_by_id(db, o.user_id)
            result.append({
                "order_id": o.id,
                "username": user.username if user else "unknown",
                "status": o.status,
                "total_price": o.total_price,
                "items": [
                    {"product_name": item.product.name, "quantity": item.quantity}
                    for item in o.items
                ],
                "created_at": str(o.created_at),
            })
        return result
    finally:
        db.close()
def tool_update_order_status(order_id: int, new_status: str):
    from app.services.chat_services import (
        create_conversation,
        get_conversations_by_user,
        save_message,
    )
    valid_statuses = {
        "pending", "preparing", "ready",
        "out_for_delivery", "delivered", "cancelled",
    }
    if new_status not in valid_statuses:
        return {"error": f"Status must be one of: {', '.join(valid_statuses)}."}
    STATUS_MESSAGES = {
        "pending": "has been received and is pending",
        "preparing": "is now being prepared",
        "ready": "is ready for pickup",
        "out_for_delivery": "is on its way to you",
        "delivered": "has been delivered",
        "cancelled": "has been cancelled",
    }
    db = SessionLocal()
    try:
        order = update_order_status(db, order_id=order_id, new_status=new_status)
        if not order:
            return {"error": f"No order found with id {order_id}."}
        # Notify the customer about the status change of their order
        conversations = get_conversations_by_user(db, user_id=order.user_id)
        conversation = conversations[0] if conversations else create_conversation(db, user_id=order.user_id)
        notification = f"Update: your order #{order.id} {STATUS_MESSAGES[new_status]}."
        save_message(db, conversation_id=conversation.id, role="assistant", content=notification)
        return {"message": f"Order #{order.id} marked as '{order.status}'. Customer notified."}
    finally:
        db.close()