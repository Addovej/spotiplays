import sqlalchemy as sa
from databases import Database

from conf import settings

__all__ = (
    'db',
    'metadata',
)

db = Database(settings.DATABASE_URL)
metadata = sa.MetaData()
