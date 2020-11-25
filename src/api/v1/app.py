from fastapi import APIRouter

from .playlists import router as playlists_router
from .spotifyd import router as spotifyd_router

__all__ = (
    'router',
)

router = APIRouter()
router.include_router(
    playlists_router,
    prefix='/playlists',
    tags=['playlists']
)
router.include_router(
    spotifyd_router,
    prefix='/spotifyd',
    tags=['spotifyd']
)
