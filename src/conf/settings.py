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
    LOGS_DIR: Path = None
    PORT: int = 8010
    SECRET_KEY: str = Fernet.generate_key()

    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    DATABASE_URL: str = None
    SPOTIFYD_CMD: list = [
        '/usr/bin/spotifyd --no-daemon',
        '--initial-volume 51',
        '--config-path /etc/spotifyd.conf'
    ]

    class Config:
        case_sensitive = True
        # Remove next line if you want use an environment variables
        env_file = '.env'

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
        return f'sqlite:///{values["BASE_DIR"]}/spotiplays.db'
