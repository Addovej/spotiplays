import secrets
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    API_ROOT: Path
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    ENVIRONMENT: str = 'LOCAL'
    LOGS_DIR: Path = None
    PORT: int = 8010
    SECRET_KEY: str = secrets.token_urlsafe(32)

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
