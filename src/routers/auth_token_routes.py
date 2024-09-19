from fastapi import APIRouter, HTTPException
from config import settings
import aiohttp

router = APIRouter()

@router.post("/auth/oauth/token/refresh")
async def refresh_access_token(refresh_token: str):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "refresh_token": refresh_token
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, data=data) as resp:
                token_info = await resp.json()

        access_token = token_info.get("access_token")
        new_refresh_token = token_info.get("refresh_token")
        expires_in = token_info.get("expires_in")

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to refresh access token")

        # If a new refresh_token is provided, you can save it instead of the old one

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "expires_in": expires_in
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Failed to refresh access token")
    