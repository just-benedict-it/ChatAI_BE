"""Add img_url column to chat_list stg 

Revision ID: b5d17de766b9
Revises: 425270acc719
Create Date: 2023-12-06 23:21:15.848573

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5d17de766b9'
down_revision: Union[str, None] = '425270acc719'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('chat_list', sa.Column('img_url', sa.String(length=255), nullable=True))
