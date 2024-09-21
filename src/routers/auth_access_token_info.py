from fastapi import APIRouter, Depends

from dependencies import oauth2_scheme
from validators import validate_access_token


router = APIRouter(tags=['Auth'])



@router.get('/auth/protected')
async def protected_route(token: str = Depends(oauth2_scheme)):
    token_info = await validate_access_token(token)
    return {'message': 'Protected content', 'token_info': token_info}
