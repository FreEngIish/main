from repositories.auth_repository import AuthRepository


class AuthTokenService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    async def refresh_access_token(self, refresh_token: str):
        return await self.auth_repository.refresh_token(refresh_token)
