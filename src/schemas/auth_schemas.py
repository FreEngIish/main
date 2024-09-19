from pydantic import BaseModel

class UserInfo(BaseModel):
    email: str
    name: str

class GoogleLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    expiration_time: float
    user_info: UserInfo

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
