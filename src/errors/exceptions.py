from logging import getLogger
from typing import Dict, Union

from fastapi import HTTPException, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

__all__ = (
    'NotFoundException',
    'LogHTTPException',
    'log_custom_http_exceptions_handler',
)

logger = getLogger('request.4XX')


class NotFoundException(HTTPException):
    def __init__(self, detail: Union[Dict, str] = None) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class LogHTTPException(HTTPException):
    def __init__(
            self,
            status: int = status.HTTP_400_BAD_REQUEST,
            detail: Union[Dict, str] = None
    ) -> None:
        super().__init__(
            status_code=status,
            detail=detail
        )


async def log_custom_http_exceptions_handler(
        request: Request, exc: LogHTTPException
) -> JSONResponse:
    logger.error(
        msg=exc.detail,
        extra={
            'status_code': exc.status_code,
            'request.method': request.method,
            'request.path': request.url.path,
            'request.headers': dict(request.headers),
        }
    )

    headers = getattr(exc, 'headers', None)
    if headers:
        return JSONResponse(
            {'detail': exc.detail},
            status_code=exc.status_code,
            headers=headers
        )
    else:
        return JSONResponse(
            {'detail': exc.detail},
            status_code=exc.status_code
        )
