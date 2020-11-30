import sqlalchemy as sa

from database import db, metadata

from .base import BaseModelInterface

__all__ = (
    'Account',
    'accounts',
    'ActiveAccount',
    'active_account',
)

active_account = sa.Table(
    'active_account',
    metadata,
    sa.Column('account_id', sa.Integer, sa.ForeignKey('accounts.id')),
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


class ActiveAccount:
    model = active_account

    @classmethod
    async def get_active(cls):
        return await db.fetch_one(
            sa.sql.select([
                active_account
            ])
        )

    @classmethod
    async def set_active(cls, account_id: int):
        res = await db.execute(
            sa.update(
                cls.model
            ).values(account_id=account_id)
        )
        if not res:
            res = await db.execute(
                sa.insert(
                    cls.model
                ).values(account_id=account_id)
            )

        return res
