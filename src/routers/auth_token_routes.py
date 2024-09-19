from fastapi import APIRouter, HTTPException

from config import settings
from repositories.auth_repository import AuthRepository
from services.auth_token_service import AuthService


router = APIRouter()
auth_repository = AuthRepository(settings.google_client_id, settings.google_client_secret, settings.google_redirect_uri)
auth_service = AuthService(auth_repository)

@router.post('/auth/oauth/token/refresh')
async def refresh_access_token(refresh_token: str):
    try:
        return await auth_service.refresh_access_token(refresh_token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

