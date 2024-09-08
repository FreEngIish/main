from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str #Secret key for hash data for authentitification
    ALGORITHM: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    # TIME_TO_RENEW_ACCESS = 30 #Time to refresh access token in MINUTES
    # TIME_TO_RENEW_REFRESH = 30 #Time to refresh access token in DAYS

settings = Settings()
