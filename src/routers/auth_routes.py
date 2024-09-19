# E:\voicenger\main-5\src\auth\google.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import aiohttp
from config import settings

router = APIRouter()

@router.get("/auth/login/google")
async def google_login():
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?client_id={settings.google_client_id}"
        f"&redirect_uri={settings.google_redirect_uri}&response_type=code"
        f"&scope=openid email profile&access_type=offline"
    )
    return RedirectResponse(url=google_auth_url)

@router.get("/auth/oauth/login-success")
async def auth_google(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": settings.google_redirect_uri,
        "grant_type": "authorization_code",
    }

    try:
        # Получение токенов
        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, data=data) as resp:
                token_info = await resp.json()
                if "access_token" not in token_info:
                    raise HTTPException(status_code=400, detail="Failed to get access token")

        access_token = token_info.get("access_token")
        refresh_token = token_info.get("refresh_token")

        # Получение информации о пользователе
        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        async with aiohttp.ClientSession() as session:
            async with session.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"}) as resp:
                user_info = await resp.json()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_info": user_info
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Failed to authenticate")
