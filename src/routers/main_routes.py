from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.__init__ import init_db
from src.db.database import database, get_db
from src.service.auth_service import get_current_user


router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/', status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):  # noqa: ARG001
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {'User': user}

@router.on_event('startup')
async def startup():
    await database.connect()
    await init_db()

@router.on_event('shutdown')
async def shutdown():
    await database.disconnect()
