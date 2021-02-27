import sqlalchemy as sa
from databases import Database

from conf import settings

__all__ = (
    'db',
    'metadata',
)

assert settings.DATABASE_URL is not None, 'DATABASE_URL must be provided'
db = Database(settings.DATABASE_URL)
metadata = sa.MetaData()
