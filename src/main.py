import logging.config

import uvicorn
from fastapi import APIRouter, FastAPI

from api import router as api_router
from conf import settings
from conf.logging import get_logging
from errors import LogHTTPException, log_custom_http_exceptions_handler
from middlewares import LoggingErrorMiddleware
from services.spotifyd import spotifyd

logging.config.dictConfig(
    get_logging(settings.LOGS_DIR)
)

params = dict(
    title='Spotiplays',
    description='Spotify playlists handler with spotify daemon',
)
if settings.ENVIRONMENT in ('DEV', 'LOCAL'):
    params.update(dict(
        redoc_url=f'{settings.API_ROOT}/redoc',
        docs_url=f'{settings.API_ROOT}/docs',
        openapi_url=f'{settings.API_ROOT}/openapi.json'
    ))
else:
    params.update(dict(
        redoc_url=None,
        docs_url=None,
        openapi_url=None
    ))

app = FastAPI(**params)
app.add_exception_handler(
    LogHTTPException, log_custom_http_exceptions_handler
)
app.add_middleware(LoggingErrorMiddleware)

api = APIRouter()
api.include_router(api_router)
app.include_router(api, prefix=str(settings.API_ROOT))


@app.on_event('startup')
async def startup():
    await spotifyd.start()


@app.on_event('shutdown')
async def shutdown():
    await spotifyd.stop()


if settings.ENVIRONMENT == 'LOCAL' and __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=settings.PORT, debug=True)
