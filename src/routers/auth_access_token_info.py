from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from validators import validate_access_token


router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login/google')

@router.get('/auth/protected')
async def protected_route(token: str = Depends(oauth2_scheme)):
    token_info = await validate_access_token(token)
    return {'message': 'Protected content', 'token_info': token_info}
