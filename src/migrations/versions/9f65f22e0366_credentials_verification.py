"""credentials_verification

Revision ID: 9f65f22e0366
Revises: c2f70be930c9
Create Date: 2020-11-28 22:37:09.789863

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '9f65f22e0366'
down_revision = 'c2f70be930c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'accounts',
        sa.Column('credentials_verification', sa.JSON(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('accounts', 'credentials_verification')
