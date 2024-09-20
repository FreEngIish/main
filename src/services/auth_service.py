import time

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.auth_repository import AuthRepository
from repositories.user_repository import UserRepository
from schemas.auth_schemas import GoogleLoginResponse, UserInfo


class AuthService:
    def __init__(self, auth_repository: AuthRepository, db: AsyncSession):
        self.auth_repository = auth_repository
        self.db = db

    async def authenticate_user(self, code: str) -> GoogleLoginResponse:
        token_info = await self.auth_repository.get_tokens(code)

        access_token = token_info.get('access_token')
        refresh_token = token_info.get('refresh_token')
        expires_in = token_info.get('expires_in')

        if not access_token:
            raise Exception('Failed to get access token')

        current_time = time.time()
        expiration_time = current_time + expires_in if expires_in else None

        user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        async with aiohttp.ClientSession() as session:
            async with session.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'}) as resp:
                user_info_data = await resp.json()

        user_info = UserInfo(
            google_sub=user_info_data['id'],
            email=user_info_data['email'],
            first_name=user_info_data.get('given_name', ''),
            last_name=user_info_data.get('family_name', ''),
            picture=user_info_data.get('picture', ''),
            locale=user_info_data.get('locale', '')
        )

        user_repo = UserRepository(self.db)
        user = await user_repo.get_user_by_email(user_info.email)
        if not user:
            user = await user_repo.create_user(
            email=user_info.email,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            google_sub = user_info.google_sub,
            picture = user_info.picture,
            locale = user_info.locale
        )

        return GoogleLoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            expiration_time=expiration_time,
            user_info=user_info
        )
