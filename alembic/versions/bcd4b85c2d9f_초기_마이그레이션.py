"""초기 마이그레이션

Revision ID: bcd4b85c2d9f
Revises: b5d17de766b9
Create Date: 2023-12-06 23:25:18.131843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcd4b85c2d9f'
down_revision: Union[str, None] = 'b5d17de766b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
