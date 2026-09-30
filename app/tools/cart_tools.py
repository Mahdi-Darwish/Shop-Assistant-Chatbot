from app.database import SessionLocal

from app.services.cart_services import (
    add_item_to_cart,
    checkout_cart,
    get_cart_with_items,
    remove_item_from_cart,
    clear_cart,
)
from app.services.products_services import search_product_by_name


def _resolve_single_product(db, product_name: str):
    """Shared helper: turns a natural-language product name into exactly
    one Product, or returns an error dict describing why it couldn't."""
    matches = search_product_by_name(db=db, name=product_name)
    if not matches:
        return None, {"error": f"No product found matching '{product_name}'."}
    if len(matches) > 1:
        return None, {
            "error": "Multiple products match that name — ask the user which one they mean.",
            "matches": [{"id": p.id, "name": p.name, "price": p.price} for p in matches],
        }
    return matches[0], None


def _cart_snapshot(db, user_id: int) -> dict:
    """The user's current cart lines + total (used by view_cart and, after
    every add_to_cart, so the chat can show the cart with Checkout /
    Add-more buttons instead of relying on the AI's wording)."""
    result = get_cart_with_items(db, user_id)
    if not result:
        return {"items": [], "total": 0.0}
    cart, items = result
    out_items = []
    total = 0.0
    for item in sorted(items, key=lambda i: i.id):
        subtotal = item.product.price * item.quantity
        total += subtotal
        out_items.append(
            {
                "product_id": item.product.id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "unit_price": item.product.price,
                "subtotal": subtotal,
                "image_url": item.product.image_url,
            }
        )
    return {"cart_id": cart.id, "items": out_items, "total": total}


def tool_add_to_cart(user_id: int, product_name: str, quantity: int = 1):
    if quantity < 1:
        return {"error": "Quantity must be at least 1."}
    db = SessionLocal()
    try:
        product, error = _resolve_single_product(db, product_name)
        if error:
            return error

        item = add_item_to_cart(db, user_id=user_id, product_id=product.id, quantity=quantity)
        return {
            "message": f"Added {quantity} x {product.name} to the cart.",
            "product_id": product.id,
            "quantity_in_cart": item.quantity,
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "image_url": product.image_url,
            },
            "cart": _cart_snapshot(db, user_id),
        }
    finally:
        db.close()


def tool_remove_from_cart(user_id: int, product_name: str, quantity: int | None = None):
    if quantity is not None and quantity < 1:
        return {"error": "Quantity must be at least 1."}
    db = SessionLocal()
    try:
        product, error = _resolve_single_product(db, product_name)
        if error:
            return error

        removed = remove_item_from_cart(
            db, user_id=user_id, product_id=product.id, quantity=quantity
        )
        if not removed:
            return {"error": f"'{product.name}' is not in the cart."}
        return {"message": f"Removed {product.name} from the cart."}
    finally:
        db.close()


def tool_view_cart(user_id: int):
    db = SessionLocal()
    try:
        snapshot = _cart_snapshot(db, user_id)
        if not snapshot["items"]:
            return {"items": [], "total": 0.0, "message": "The cart is empty."}
        return snapshot
    finally:
        db.close()


def tool_checkout_cart(user_id: int):
    db = SessionLocal()
    try:
        order = checkout_cart(db, user_id=user_id)
        if not order:
            return {"error": "The cart is empty — nothing to check out."}
        return {
            "message": "Order placed successfully.",
            "order_id": order.id,
            "status": order.status,
            "total_price": order.total_price,
            "items": [
                {
                    "product_name": oi.product.name,
                    "quantity": oi.quantity,
                    "unit_price": oi.price_at_purchase,
                    "subtotal": oi.price_at_purchase * oi.quantity,
                    "image_url": oi.product.image_url,
                }
                for oi in order.items
            ],
        }
    finally:
        db.close()
def tool_clear_cart(user_id:int):
    db = SessionLocal()
    try:
        clear_cart(db,user_id=user_id)
        return {"message":"Your cart has been cleared."}
    finally:
        db.close()