
from fastapi import APIRouter, HTTPException, status

from src.db.__init__ import init_db
from src.db.database import database
from src.dependencies import db_dependency, user_dependency


router = APIRouter()

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
