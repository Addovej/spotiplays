from typing import Optional, Union

import sqlalchemy as sa
from sqlalchemy.engine.result import RowProxy

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
    sa.Column('credentials_verification', sa.JSON, nullable=True),
)


class Account(BaseModelInterface):
    model = accounts

    @classmethod
    async def create(cls, **kwargs: Union[str, int, dict]) -> int:
        # TODO: Change it to call API for verify.
        verification = {'state': 'OK', 'details': ''}
        return await super().create(
            credentials_verification=verification,
            **kwargs
        )

    @classmethod
    async def change_credentials_verification(
            cls, pk: int, data: dict[str, str]
    ) -> int:
        return await cls.update(
            pk=pk, credentials_verification=data
        )


class ActiveAccount:
    model = active_account

    @classmethod
    async def get_active(cls) -> Optional[RowProxy]:
        return await db.fetch_one(
            sa.sql.select([
                active_account
            ])
        )

    @classmethod
    async def set_active(cls, account_id: int) -> int:
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
