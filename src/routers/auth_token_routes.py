import logging

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_auth_token_service
from services.auth_token_service import AuthService


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=['Auth'])

@router.post('/auth/oauth/token/refresh')
async def refresh_access_token(refresh_token: str, auth_service: AuthService = Depends(get_auth_token_service)):
    try:
        response = await auth_service.refresh_access_token(refresh_token)
        return response
    except Exception as e:
        # Log any other exceptions
        logger.error(f'Error during token refresh: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))
