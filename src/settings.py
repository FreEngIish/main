from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str #Secret key for hash data for authentitification
    ALGORITHM: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
