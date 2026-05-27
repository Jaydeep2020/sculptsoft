"""add user role

Revision ID: f096ac8e3d6d
Revises: 6341c5186c82
Create Date: 2026-05-26 15:42:36.621784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f096ac8e3d6d'
down_revision: Union[str, Sequence[str], None] = '6341c5186c82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_role = sa.Enum(
    'ADMIN',
    'STAFF',
    name='user_role'
)

def upgrade():

    user_role.create(op.get_bind())

    op.add_column(
        'users',
        sa.Column(
            'role',
            user_role,
            nullable=False,
            server_default='STAFF'
        )
    )


def downgrade():

    op.drop_column('users', 'role')

    user_role.drop(op.get_bind())
