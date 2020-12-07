from pydantic import BaseModel, validator

from utils import decrypt, encrypt

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


class CredentialsVerification(BaseModel):
    state: str
    details: str


class AccountSchema(_Base, _Password):
    id: int
    credentials_verification: CredentialsVerification

    class Config:
        fields = {
            'id': {
                'title': 'Account ID'
            },
            'credentials_verification': {
                'title': 'Account credential verification data'
            },
            **_Base.Config.fields,
            **_Password.Config.fields
        }

    def password_decrypted(self) -> str:
        return decrypt(self.password)

    def is_verified(self) -> bool:
        return self.credentials_verification.state == 'OK'


class CreateAccountSchema(_Base, _Password):

    class Config:
        fields = {
            **_Base.Config.fields,
            **_Password.Config.fields
        }

    @validator('password', pre=True)
    def encrypt_password(cls, v: str) -> str:
        return encrypt(v)


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
    credentials_verification: CredentialsVerification

    class Config:
        fields = {
            'id': {
                'title': 'Account ID'
            },
            'credentials_verification': {
                'title': 'Account credential verification data'
            },
            **_Base.Config.fields
        }


class GetListAccountSchema(BaseModel):
    items: list[GetAccountSchema]
