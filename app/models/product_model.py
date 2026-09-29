from sqlalchemy import Column, Float, Integer, String
from app.database import Base

class Product(Base):
    __tablename__ ='products'
    id = Column(Integer,primary_key=True,index=True)
    name =Column(String)
    description=Column(String)
    price = Column(Float)
    # Relative path like /uploads/products/<uuid>.jpg (uploaded from the admin's
    # device) or a full https:// link. NULL = no image; the UI shows a fallback.
    image_url = Column(String, nullable=True)



