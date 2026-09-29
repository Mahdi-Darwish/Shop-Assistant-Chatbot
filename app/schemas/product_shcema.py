from pydantic import BaseModel, ConfigDict, field_validator
from app.services.image_services import is_valid_image_url


def _check_image_url(v: str | None) -> str | None:
    if v is None:
        return None
    v = v.strip()
    if not v:
        return None
    if not is_valid_image_url(v):
        raise ValueError("image_url must be an uploaded image or an http(s) link")
    return v


class ProductSchema(BaseModel):
    id:int | None = None
    name:str
    description:str
    price:float
    image_url:str | None = None
    model_config =ConfigDict(from_attributes=True)
class ProductCreate(BaseModel):
    name:str
    description:str
    price:float
    image_url:str | None = None

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls,v:float) ->float:
        if v<=0:
            raise ValueError("Price must be greater than zero")
        return v

    @field_validator("image_url")
    @classmethod
    def image_url_valid(cls, v: str | None) -> str | None:
        return _check_image_url(v)
class ProductUpdate(BaseModel):
    """All fields optional — this is a PATCH, an admin can update just
    the price without resending everything else."""
 
    name: str | None = None
    description: str | None = None
    price: float | None = None
    image_url: str | None = None
 
    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: float | None) -> float | None:
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than zero")
        return v

    @field_validator("image_url")
    @classmethod
    def image_url_valid(cls, v: str | None) -> str | None:
        return _check_image_url(v)
