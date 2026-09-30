from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile, status
from sqlalchemy.orm import Session
from app.core.rate_limit import limiter
from app.dependencies import get_db, require_admin
from app.models.user_model import User
from app.schemas.product_shcema import ProductSchema as ProductOut, ProductCreate,ProductUpdate
from app.schemas.order_schema import AdminOrderItemOut, AdminOrderOut, OrderStatusUpdate
from app.schemas.user_schema import UserOut
from app.services.order_services import (
    get_order_with_customer,
    get_orders_with_customers,
    update_order_status_and_notify,
)
from app.services.image_services import save_product_image
from app.services.products_services import (
    create_product,
    delete_product,
    get_products,
    update_product,
)
from app.services.user_services import (
    delete_user,
    all_users as get_all_users,
    set_user_active_status,
    set_user_role,
)
router = APIRouter(prefix="/admin", tags=["admin"])
#users
@router.get("/users", response_model=list[UserOut])
@limiter.limit("60/minute")
def list_all_users(
    request:Request,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Only reachable by role == 'admin'. There is no chatbot tool that
    maps to this — the LLM has no path to ever call it."""
    return get_all_users(db)

@router.patch("/users/{user_id}/deactivate", response_model=UserOut)
@limiter.limit("20/minute")
def deactivate_user_route(
    request:Request,
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    user = set_user_active_status(db, user_id=user_id, is_active=False)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

@router.patch("/users/{user_id}/activate", response_model=UserOut)
@limiter.limit("20/minute")
def activate_user_route(
    request:Request,
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    user = set_user_active_status(db, user_id=user_id, is_active=True)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

@router.patch("/users/{user_id}/promote", response_model=UserOut)
@limiter.limit("20/minute")
def promote_user_route(
    request:Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """Grants admin access — this, along with 'delete', is deliberately
    NOT reachable through the admin chatbot. The single most sensitive
    action in the system stays behind an explicit Swagger/form action,
    not something a cleverly worded chat message could ever trigger."""
    user = set_user_role(db, user_id=user_id, role="admin")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

@router.patch("/users/{user_id}/demote", response_model=UserOut)
@limiter.limit("20/minute")
def demote_user_route(
    request:Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    if user_id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You can't demote your own account — ask another admin to do it.",
        )
    user = set_user_role(db, user_id=user_id, role="customer")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

@router.delete("/users/{user_id}")
@limiter.limit("10/minute")
def delete_user_route(
    request:Request,
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    success, message = delete_user(db, user_id=user_id)
    if not success:
        code = status.HTTP_404_NOT_FOUND if message == "User not found." else status.HTTP_409_CONFLICT
        raise HTTPException(status_code=code, detail=message)
    return {"message": message}
#products

@router.get("/products", response_model=list[ProductOut])
@limiter.limit("60/minute")
def list_products_admin(
    request:Request,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return get_products(db)

@router.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
def add_product(
    request:Request,
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return create_product(
        db,
        name=payload.name,
        description=payload.description,
        price=payload.price,
        image_url=payload.image_url,
    )

@router.post("/uploads/product-image", status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
async def upload_product_image(
    request: Request,
    file: UploadFile = File(...),
    _admin: User = Depends(require_admin),
):
    """Step 1 of adding a product with a photo from the admin's device.
    Returns {"image_url": "/uploads/products/<id>.jpg"}; that value is then
    sent as `image_url` on POST/PATCH /admin/products, or as `image_url` in
    the admin chat request."""
    return {"image_url": await save_product_image(file)}

@router.patch("/products/{product_id}", response_model=ProductOut)
@limiter.limit("20/minute")
def edit_product(
    request:Request,
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    product = update_product(
        db,
        product_id=product_id,
        name=payload.name,
        description=payload.description,
        price=payload.price,
        image_url=payload.image_url,
    )
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    return product

@router.delete("/products/{product_id}")
@limiter.limit("10/minute")
def remove_product(
    request:Request,
    product_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    success, message = delete_product(db, product_id=product_id)
    if not success:
        code = (
            status.HTTP_404_NOT_FOUND
            if message == "Product not found."
            else status.HTTP_409_CONFLICT
        )
        raise HTTPException(status_code=code, detail=message)
    return {"message": message}

#orders (live board in the admin dashboard)
def _order_out(order, user) -> AdminOrderOut:
    items = []
    for oi in sorted(order.items, key=lambda i: i.id):
        product = oi.product
        items.append(
            AdminOrderItemOut(
                product_name=product.name if product else "(removed item)",
                quantity=oi.quantity,
                unit_price=oi.price_at_purchase,
                subtotal=oi.price_at_purchase * oi.quantity,
                image_url=product.image_url if product else None,
            )
        )
    return AdminOrderOut(
        id=order.id,
        username=user.username,
        phone=user.phone,
        status=order.status,
        total_price=order.total_price,
        created_at=order.created_at,
        items=items,
    )

@router.get("/orders", response_model=list[AdminOrderOut])
@limiter.limit("120/minute")
def list_orders_admin(
    request: Request,
    limit: int = Query(200, ge=1, le=500),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Newest first. The dashboard polls this every few seconds so new
    orders appear without the admin having to ask the chatbot."""
    return [_order_out(order, user) for order, user in get_orders_with_customers(db, limit=limit)]

@router.patch("/orders/{order_id}/status", response_model=AdminOrderOut)
@limiter.limit("60/minute")
def set_order_status_admin(
    request: Request,
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    order, error = update_order_status_and_notify(db, order_id=order_id, new_status=payload.status)
    if error:
        code = status.HTTP_404_NOT_FOUND if error.startswith("No order") else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=error)
    row = get_order_with_customer(db, order_id)
    return _order_out(*row)

