from sqlalchemy import Column, DateTime, LargeBinary, String, func
from app.database import Base


class ProductImage(Base):
    """A product photo stored inside Postgres (bytea), so it survives
    Render restarts and redeploys — unlike files on Render's temporary disk.

    `id` is the 32-character hex name that appears in Product.image_url,
    e.g. /uploads/products/<id>.jpg
    """
    __tablename__ = "product_images"

    id = Column(String(32), primary_key=True)
    content_type = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
