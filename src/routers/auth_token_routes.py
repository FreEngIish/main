import logging

from fastapi import APIRouter, HTTPException

from config import settings
from repositories.auth_repository import AuthRepository
from services.auth_token_service import AuthService


# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
auth_repository = AuthRepository(settings.google_client_id, settings.google_client_secret, settings.google_redirect_uri)
auth_service = AuthService(auth_repository)

@router.post('/auth/oauth/token/refresh')
async def refresh_access_token(refresh_token: str):
    logger.info(f'Received request to refresh token: {refresh_token}')
    try:
        response = await auth_service.refresh_access_token(refresh_token)
        logger.info('Token successfully refreshed.')
        return response
    except HTTPException as e:
        logger.error(f'HTTPException during token refresh: {e.detail}')
        raise e
    except Exception as e:
        logger.error(f'Error during token refresh: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))
