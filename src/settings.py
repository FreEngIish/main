from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str #Secret key for hash data for authentitification
    ALGORITHM: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
