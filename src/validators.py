import aiohttp
from fastapi import HTTPException


async def validate_access_token(token: str):
    async with aiohttp.ClientSession() as session:
        url = f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}'
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=401, detail='Invalid access token')
            return await response.json()
