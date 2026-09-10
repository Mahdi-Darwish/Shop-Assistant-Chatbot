from pydantic import BaseModel, ConfigDict, field_validator
class ProductSchema(BaseModel):
    id:int | None = None
    name:str
    description:str
    price:float
    model_config =ConfigDict(from_attributes=True)
class ProductCreate(BaseModel):
    name:str
    description:str
    price:float

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls,v:float) ->float:
        if v<=0:
            raise ValueError("Price must be greater than zero")
        return v
class ProductUpdate(BaseModel):
    """All fields optional — this is a PATCH, an admin can update just
    the price without resending everything else."""
 
    name: str | None = None
    description: str | None = None
    price: float | None = None
 
    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: float | None) -> float | None:
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than zero")
        return v