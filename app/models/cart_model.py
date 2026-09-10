from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, func, text
from sqlalchemy.orm import relationship
from app.database import Base
class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String, nullable=False, default="active")  # active | checked_out | cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    __table_args__ = (
        Index(
            "uq_one_active_cart_per_user",
            "user_id",
            unique=True,
            postgresql_where=text("status = 'active'"),
        ),
    )
class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
    __table_args__ = (
        Index("uq_cart_product", "cart_id", "product_id", unique=True),
    )