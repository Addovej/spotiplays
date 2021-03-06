from pathlib import Path

import toml
from cryptography.fernet import Fernet

from conf import settings


def decrypt(value: str) -> str:
    f = Fernet(settings.SECRET_KEY)
    return f.decrypt(value.encode()).decode()


def encrypt(value: str) -> str:
    f = Fernet(settings.SECRET_KEY)
    return f.encrypt(value.encode()).decode()


async def generate_spotifyd_conf() -> None:
    """
    Generate spotifyd.conf toml config from
    CONF_ prefixed settings.
    """

    if not Path(settings.CONFIG_PATH).exists() or settings.FORCE_GENERATE:
        conf: dict[str, str] = {}
        need_slugify: tuple[str, ...] = (
            'VOLUME_CONTROLLER',
            'VOLUME_NORMALISATION',
            'NORMALISATION_PREGAIN',
        )

        for key, value in settings.dict().items():
            if key.startswith('CONF_'):
                *_, _key = key.partition('_')

                # For some reason spotifyd could not recognize
                #   these keys in snake case.
                #   Therefore makes some slugify.
                if _key in need_slugify:
                    _key = _key.replace('_', '-')

                conf[_key.lower()] = value

        if conf:
            with open(settings.CONFIG_PATH, 'w') as f:
                toml.dump({'global': conf}, f)
