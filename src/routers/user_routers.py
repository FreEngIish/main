import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from dependencies import get_user_service
from schemas.auth_schemas import CreateUserRequest, ShowUser
from service.user_service import UserService


logger = logging.getLogger(__name__)

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def create_user(user_data: CreateUserRequest, user_service: UserService = Depends(get_user_service)) -> ShowUser:
    """
    Create a new user.

    This endpoint registers a new user in the database.
    """
    try:
        return await user_service.create_user(create_user_request=user_data)

    except IntegrityError as err:
        logger.error(f'Integrity error: {err}')
        raise HTTPException(status_code=400, detail=f'Database error: {err}')


# @router.get('/', status_code=status.HTTP_200_OK)
# async def user(user: user_dependency, db: db_dependency):  # noqa: ARG001
#     if user is None:
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     return {'User': user}
