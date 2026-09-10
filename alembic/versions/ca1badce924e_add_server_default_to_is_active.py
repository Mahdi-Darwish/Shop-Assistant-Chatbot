"""add server default to is_active

Revision ID: ca1badce924e
Revises: 251716ceb2e8
Create Date: 2026-09-07 12:38:58.478422

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca1badce924e'
down_revision: Union[str, Sequence[str], None] = '251716ceb2e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'is_active', server_default=sa.text('true'))


def downgrade() -> None:
    op.alter_column('users', 'is_active', server_default=None)