import re
from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / 'test.db'
LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Z0-9\-]+$")

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_URL: str = f'sqlite+aiosqlite:///{DB_PATH}'
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
