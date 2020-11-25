import sqlalchemy as sa

from database import metadata

from .base import BaseModelInterface

__all__ = (
    'Account',
    'accounts',
)

accounts = sa.Table(
    'accounts',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(45)),
    sa.Column('username', sa.String(45), unique=True),
    sa.Column('password', sa.String(45)),
)


class Account(BaseModelInterface):
    model = accounts
