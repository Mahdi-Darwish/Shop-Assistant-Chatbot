from datetime import datetime
from pydantic import BaseModel, ConfigDict
class OrderItemOutSchema(BaseModel):
    product_id :int
    produc_name:int
    quantity:int
    price_at_purchase : float
    model_config = ConfigDict(from_attributes=True)
class OrderOutSchema(BaseModel):
    order_id : int
    status : str
    created_at : datetime
    items: list[OrderItemOutSchema]
    total: float


# ---- Admin dashboard (live orders board) ----
class AdminOrderItemOut(BaseModel):
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float
    image_url: str | None = None

class AdminOrderOut(BaseModel):
    id: int
    username: str
    phone: str | None = None
    status: str
    total_price: float
    created_at: datetime | None = None
    items: list[AdminOrderItemOut]

class OrderStatusUpdate(BaseModel):
    status: str

