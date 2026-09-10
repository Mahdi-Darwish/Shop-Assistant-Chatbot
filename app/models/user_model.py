from sqlalchemy import Column, DateTime, Integer, String, func,Boolean
from app.database import Base
from sqlalchemy import Column, DateTime, Integer, String, func, Boolean, text
from app.database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    role = Column(String, nullable=False, default='customer')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
