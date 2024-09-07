from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = '12345'
    ALGORITHM: str = 'HS256'

settings = Settings()
