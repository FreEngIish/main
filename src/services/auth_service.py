import aiohttp
from repositories.auth_repository import AuthRepository
from schemas.auth_schemas import GoogleLoginResponse
import time

class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    async def authenticate_user(self, code: str) -> GoogleLoginResponse:
        token_info = await self.auth_repository.get_tokens(code)

        access_token = token_info.get("access_token")
        refresh_token = token_info.get("refresh_token")
        expires_in = token_info.get("expires_in")

        if not access_token:
            raise Exception("Failed to get access token")

        current_time = time.time()
        expiration_time = current_time + expires_in if expires_in else None

        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        async with aiohttp.ClientSession() as session:
            async with session.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"}) as resp:
                user_info = await resp.json()

        return GoogleLoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            expiration_time=expiration_time,
            user_info=user_info
        )
