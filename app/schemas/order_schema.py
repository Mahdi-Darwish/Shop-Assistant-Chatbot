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