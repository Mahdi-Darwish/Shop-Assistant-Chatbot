from sqlalchemy import Column, Float, Integer, String
from app.database import Base

class Product(Base):
    __tablename__ ='products'
    id = Column(Integer,primary_key=True,index=True)
    name =Column(String)
    description=Column(String)
    price = Column(Float)



