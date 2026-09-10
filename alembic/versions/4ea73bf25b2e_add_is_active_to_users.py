# """add is_active to users

# Revision ID: 4ea73bf25b2e
# Revises: b54c5af2a65c
# Create Date: 2026-09-07 12:23:30.458963

# """
# from typing import Sequence, Union

# from alembic import op
# import sqlalchemy as sa


# # revision identifiers, used by Alembic.
# revision: str = '4ea73bf25b2e'
# down_revision: Union[str, Sequence[str], None] = 'b54c5af2a65c'
# branch_labels: Union[str, Sequence[str], None] = None
# depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     op.alter_column('users', 'is_active',
#                existing_type=sa.BOOLEAN(),
#                nullable=False,
#                server_default=sa.text('true'))

# def downgrade() -> None:
#     op.alter_column('users', 'is_active',
#                existing_type=sa.BOOLEAN(),
#                nullable=True,
#                server_default=None)
"""add is_active to users

Revision ID: 4ea73bf25b2e
Revises: b54c5af2a65c
Create Date: 2026-09-07 12:23:30.458963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ea73bf25b2e'
down_revision: Union[str, Sequence[str], None] = 'b54c5af2a65c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
    )

def downgrade() -> None:
    op.drop_column('users', 'is_active')