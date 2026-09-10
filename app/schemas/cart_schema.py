from pydantic import BaseModel,ConfigDict
class CartItemOutSchema(BaseModel):
    product_id :int
    product_name:str
    quantity:int
    sub_total :float
    unit_price :float
    model_config = ConfigDict(from_attributes=True)

class CartOutSchema(BaseModel):
    cart_id :int
    items: list[CartItemOutSchema]
    total: float