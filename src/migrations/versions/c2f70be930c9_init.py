"""init

Revision ID: c2f70be930c9
Revises:
Create Date: 2020-11-28 15:23:23.800560

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c2f70be930c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=45), nullable=True),
        sa.Column('username', sa.String(length=45), nullable=True),
        sa.Column('password', sa.String(length=45), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.create_table(
        'active_account',
        sa.Column('account_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], )
    )


def downgrade() -> None:
    op.drop_table('active_account')
    op.drop_table('accounts')
