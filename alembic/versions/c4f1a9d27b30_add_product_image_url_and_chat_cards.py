"""add products.image_url and chat_messages.cards

Revision ID: c4f1a9d27b30
Revises: ca1badce924e
Create Date: 2026-09-29 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4f1a9d27b30'
down_revision: Union[str, Sequence[str], None] = 'ca1badce924e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Both columns are nullable, so existing rows are untouched."""
    op.add_column('products', sa.Column('image_url', sa.String(), nullable=True))
    op.add_column('chat_messages', sa.Column('cards', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('chat_messages', 'cards')
    op.drop_column('products', 'image_url')
