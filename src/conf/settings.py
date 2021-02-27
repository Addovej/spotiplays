from pathlib import Path
from typing import Any, Dict, Optional

from cryptography.fernet import Fernet
from pydantic import BaseSettings, validator

__all__ = (
    'Settings',
)


class Settings(BaseSettings):
    API_ROOT: Path
    BASE_DIR: Path = Path(__file__).parent.parent
    ENVIRONMENT: str = 'LOCAL'
    LOGS_DIR: Path
    PORT: int = 8010
    SECRET_KEY: str = str(Fernet.generate_key())

    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    DATABASE_URL: Optional[str]
    SPOTIFYD_CMD: list[str] = ['/usr/bin/spotifyd --no-daemon']

    # spotifyd.conf
    FORCE_GENERATE: bool = True
    INITIAL_VOLUME: int = 51
    CONFIG_PATH: str = '/etc/spotifyd.conf'  # Default path

    CONF_BACKEND: str = 'alsa'
    CONF_DEVICE: str = 'default'
    CONF_MIXER: str = 'PCM'
    CONF_VOLUME_CONTROLLER: str = 'alsa'
    CONF_DEVICE_NAME: str = 'SpotiPlays'
    CONF_BITRATE: int = 320
    CONF_CACHE_PATH: str = '/tmp'
    CONF_NO_AUDIO_CACHE: bool = False
    CONF_VOLUME_NORMALISATION: bool = True
    CONF_NORMALISATION_PREGAIN: int = -10
    CONF_DEVICE_TYPE: str = 'speaker'

    class Config:
        case_sensitive = True

    @validator('LOGS_DIR', pre=True)
    def create_logs_dir(
            cls, v: Optional[Path], values: Dict[str, Any]
    ) -> Path:
        if v is not None:
            log_dir = Path(v)
        else:
            log_dir = values['BASE_DIR'].joinpath('logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

    @validator('DATABASE_URL', pre=True)
    def create_db_url(
            cls, v: Optional[str], values: Dict[str, Any]
    ) -> str:
        if v is None:
            return f'sqlite:///{values["BASE_DIR"]}/data/spotiplays.db'

        return v
