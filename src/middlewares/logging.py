import logging
import typing
from traceback import TracebackException

from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR
)

__all__ = (
    'LoggingErrorMiddleware',
)

RequestResponseEndpoint = typing.Callable[
    [Request], typing.Awaitable[Response]
]

logger = logging.getLogger('request.5XX')


class LoggingErrorMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            response = await call_next(request)
        except Exception as e:
            tb = TracebackException.from_exception(e)
            logger.error(
                msg=str(e),
                extra={
                    'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                    'request.method': request.method,
                    'request.path': request.url.path,
                    'request.headers': dict(request.headers),
                    'traceback': ''.join(tb.format())
                }
            )
            return JSONResponse({
                'detail': [{
                    'type': f'Unexpected error: [{type(e).__name__}]',
                    'msg': str(e)
                }]
            }, status_code=HTTP_400_BAD_REQUEST)

        return response
