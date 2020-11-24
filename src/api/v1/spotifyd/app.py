from fastapi import APIRouter

from services.spotifyd import spotifyd

router = APIRouter()


@router.get('/current')
async def current():
    return {'username': spotifyd.user}
