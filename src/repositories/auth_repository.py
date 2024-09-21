import aiohttp
from fastapi import HTTPException


class AuthRepository:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    async def get_tokens(self, code):
        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code',
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, data=data) as resp:
                token_info = await resp.json()

        if 'error' in token_info:
            raise HTTPException(status_code=400, detail=token_info['error'])

        return token_info

    async def refresh_token(self, refresh_token):
        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, data=data) as resp:
                token_info = await resp.json()

        if 'error' in token_info:
            raise HTTPException(status_code=400, detail=token_info['error'])

        return token_info
