from typing import Any, Union
from uuid import UUID

import sqlalchemy as sa

from database import db

__all__ = (
    'BaseModelInterface',
)

PK = Union[int, UUID]


class BaseModelInterface:
    model = None

    @classmethod
    async def get_by_id(cls, pk: PK):
        return await db.fetch_one(
            sa.sql.select([
                cls.model
            ]).where(
                cls.model.c.id == pk
            )
        )

    @classmethod
    async def get_by_col_name(cls, col_name: str, value: Any):
        return await db.fetch_one(
            sa.sql.select([
                cls.model
            ]).where(
                col_name == value
            )
        )

    @classmethod
    async def get_list(cls, limit: int = 10, offset: int = 0):
        return await db.fetch_all(
            sa.sql.select([
                cls.model
            ]).limit(limit).offset(offset)
        )

    @classmethod
    async def create(cls, **kwargs):
        return await db.execute(
            sa.insert(
                cls.model
            ).values(**kwargs)
        )

    @classmethod
    async def update(cls, pk: PK, **kwargs):
        return await db.execute(
            sa.update(
                cls.model
            ).where(
                cls.model.c.id == pk
            ).values(
                **kwargs
            )
        )

    @classmethod
    async def delete(cls, pk: PK):
        return await db.execute(
            sa.delete(
                cls.model
            ).where(
                cls.model.c.id == pk
            )
        )
