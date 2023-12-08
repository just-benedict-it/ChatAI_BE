"""stg img_url add

Revision ID: 4c38660a540f
Revises: bcd4b85c2d9f
Create Date: 2023-12-08 21:48:05.392362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c38660a540f'
down_revision: Union[str, None] = 'bcd4b85c2d9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
