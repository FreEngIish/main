from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str



class TokenData(BaseModel):
    user_id: Optional[int] = None

    class Config:
        orm_mode = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str
