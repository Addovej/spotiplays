from fastapi import APIRouter, status
from sqlalchemy.engine.result import RowProxy

from errors import LogHTTPException, NotFoundException
from models import Account
from services.spotifyd import spotifyd

from .schemas import (
    AccountSchema,
    CreateAccountSchema,
    GetAccountSchema,
    GetListAccountSchema,
    UpdateAccountSchema
)

__all__ = (
    'router',
)

router = APIRouter()


# Accounts CRUD

@router.post(
    '/accounts',
    summary='Add a new Spotify account'
)
async def account_create(account: CreateAccountSchema) -> dict[str, int]:
    res = await Account.create(**account.dict())

    return {'id': res}


@router.get(
    '/accounts',
    summary='Get accounts list',
    response_model=GetListAccountSchema
)
async def account_list() -> dict[str, list[dict]]:
    res = await Account.get_list(limit=50)

    return {
        'items': [GetAccountSchema.parse_obj(item).dict() for item in res]
    }


@router.get(
    '/accounts/{account_id}',
    summary='Get account by ID',
    response_model=GetAccountSchema
)
async def account_get(account_id: int) -> RowProxy:
    res = await Account.get_by_id(account_id)
    if not res:
        raise NotFoundException(
            f'Not found account with {account_id!r} ID'
        )

    return res


@router.put(
    '/accounts/{account_id}',
    summary='Update account by ID'
)
async def account_update(
        account_id: int, account: UpdateAccountSchema
) -> dict[str, int]:
    res = await Account.update(account_id, **account.dict(exclude_none=True))
    if not res:
        raise NotFoundException(
            f'Not found account with {account_id!r} ID'
        )

    return {'result': res}


@router.delete(
    '/accounts/{account_id}',
    summary='Delete account by ID'
)
async def account_delete(account_id: int) -> dict[str, int]:
    res = await Account.delete(account_id)
    if not res:
        raise NotFoundException(
            f'Not found account with {account_id!r} ID'
        )

    return {'result': res}


# Spotifyd handle

@router.post(
    '/switch/{account_id}',
    summary='Switch Spotify account by ID'
)
async def switch(account_id: int) -> dict:
    res = await Account.get_by_id(account_id)
    if not res:
        raise NotFoundException(
            f'Not found account with {account_id!r} ID'
        )

    account = AccountSchema.parse_obj(res)
    if not account.is_verified():
        raise LogHTTPException(
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                'message': 'Account verification failed. '
                           'Check your spotify credentials'
            }
        )

    await spotifyd.restart(account)
    if spotifyd.errors:
        raise LogHTTPException(detail={'errors': spotifyd.errors})

    return spotifyd.user


@router.get(
    '/current',
    summary='Get current spotifyd account name'
)
async def current() -> dict:
    return spotifyd.user
