"""store product images in the database

Revision ID: d7a3b8e51f42
Revises: c4f1a9d27b30
Create Date: 2026-09-29 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7a3b8e51f42'
down_revision: Union[str, Sequence[str], None] = 'c4f1a9d27b30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'product_images',
        sa.Column('id', sa.String(length=32), primary_key=True),
        sa.Column('content_type', sa.String(), nullable=False),
        sa.Column('data', sa.LargeBinary(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    # Photos saved before this migration lived on the server's temporary disk
    # and are already gone. Clear those dead links so products fall back to
    # the default picture instead of showing a broken image; re-attach a photo
    # with the admin chat to give a product its own picture again.
    op.execute("UPDATE products SET image_url = NULL WHERE image_url LIKE '/uploads/products/%'")


def downgrade() -> None:
    op.drop_table('product_images')
