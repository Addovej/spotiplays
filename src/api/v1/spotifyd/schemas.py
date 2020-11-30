from cryptography.fernet import Fernet
from pydantic import BaseModel, validator

from conf import settings

__all__ = (
    'AccountSchema',
    'CreateAccountSchema',
    'UpdateAccountSchema',
    'GetAccountSchema',
    'GetListAccountSchema',
)


class _Base(BaseModel):
    name: str
    username: str

    class Config:
        fields = {
            'name': {
                'title': 'Account name',
                'example': 'Me'
            },
            'username': {
                'title': 'Spotify username',
                'example': 'username'
            }
        }


class _Password(BaseModel):
    password: str

    class Config:
        fields = {
            'password': {
                'title': 'Spotify account password',
                'example': 'password'
            }
        }


class AccountSchema(_Base, _Password):
    id: int

    class Config:
        fields = {
            'id': {
                'title': 'Account ID'
            },
            **_Base.Config.fields,
            **_Password.Config.fields
        }

    def password_decrypted(self) -> str:
        f = Fernet(settings.SECRET_KEY)
        return f.decrypt(self.password.encode()).decode()


class CreateAccountSchema(_Base, _Password):

    class Config:
        fields = {
            **_Base.Config.fields,
            **_Password.Config.fields
        }

    @validator('password', pre=True)
    def encrypt_password(cls, v: str) -> str:
        f = Fernet(settings.SECRET_KEY)
        return f.encrypt(v.encode()).decode()


class UpdateAccountSchema(_Base, _Password):
    name: str = None
    username: str = None
    password: str = None

    class Config:
        fields = {
            **_Base.Config.fields,
            **_Password.Config.fields
        }


class GetAccountSchema(_Base):
    id: int

    class Config:
        fields = {
            'id': {
                'title': 'Account ID'
            },
            **_Base.Config.fields
        }


class GetListAccountSchema(BaseModel):
    items: list[GetAccountSchema]
