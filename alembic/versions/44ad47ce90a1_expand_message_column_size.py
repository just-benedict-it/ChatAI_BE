"""expand message column size

Revision ID: 44ad47ce90a1
Revises: c888456a7ebc
Create Date: 2023-10-27 12:01:39.436210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44ad47ce90a1'
down_revision: Union[str, None] = 'c888456a7ebc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('chat_history', 'message',
                existing_type=sa.String(length=1000),
                type_=sa.String(length=10000),
                existing_nullable=True)


def downgrade() -> None:
    pass
