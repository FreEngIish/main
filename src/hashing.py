import logging

from passlib.context import CryptContext


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('passlib')
logger.setLevel(logging.ERROR)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
