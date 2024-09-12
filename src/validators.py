import re
from config import LETTER_MATCH_PATTERN

def validate_password(cls, value: str) -> str:
    if not re.search(r'[A-Z]', value):
        raise ValueError('Password must contain at least one uppercase letter')
    if not re.search(r'[a-z]', value):
        raise ValueError('Password must contain at least one lowercase letter')
    if not re.search(r'\d', value):
        raise ValueError('Password must contain at least one digit')
    return value


def validate_username(cls, value: str) -> str:
    if not LETTER_MATCH_PATTERN.match(value):
        raise ValueError('Username can only contain letters and numbers')
    return value
