import re
from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / 'test.db'
LETTER_MATCH_PATTERN = re.compile(r'^[a-zA-Z0-9\-]+$')

class Settings(BaseSettings):
    DATABASE_URL: str = f'sqlite+aiosqlite:///{DB_PATH}'
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
