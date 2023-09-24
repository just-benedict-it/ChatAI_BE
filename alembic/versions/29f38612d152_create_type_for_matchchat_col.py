"""create type for MatchChat col

Revision ID: 29f38612d152
Revises: 
Create Date: 2023-08-24 21:24:10.080773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29f38612d152'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# 앞서 생성했던 버전의 upgrade 함수를 수정
def upgrade():
    op.add_column('match.chat', sa.Column('type', sa.Integer(), nullable=True))

def downgrade() -> None:
    op.drop_column('match.chat', 'type')
