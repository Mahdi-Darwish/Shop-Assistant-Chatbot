from sqlalchemy import Column,Integer,Float,String,DateTime,func,ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ ='orders'
    id = Column(Integer,primary_key=True,index=True)
    user_id =Column(Integer,ForeignKey('users.id'),nullable=False,index=True)
    status = Column(String,nullable=False,default='pending')
    total_price = Column(Float,nullable=False,default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    items = relationship("OrderItem",back_populates="order",cascade="all,delete-orphan")

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")