"""stg img_url add

Revision ID: 7075eee014f0
Revises: 
Create Date: 2023-12-08 21:50:12.597542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7075eee014f0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('chat_list', sa.Column('img_url', sa.String(length=255), nullable=True))

def downgrade() -> None:
    pass
