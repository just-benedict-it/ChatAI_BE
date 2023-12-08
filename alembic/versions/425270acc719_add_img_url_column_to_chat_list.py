"""Add img_url column to chat_list

Revision ID: 425270acc719
Revises: 44ad47ce90a1
Create Date: 2023-12-06 22:35:59.598475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '425270acc719'
down_revision: Union[str, None] = '44ad47ce90a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('chat_list', sa.Column('img_url', sa.String(length=255), nullable=True))


