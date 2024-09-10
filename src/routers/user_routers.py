import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from db.models.user import User
from dependencies import get_current_user, get_user_service
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


@router.get('/', status_code=status.HTTP_200_OK, response_model=ShowUser)
async def get_user(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> ShowUser:
    """
    Retrieve the details of the current user.

    This endpoint returns the details of the currently authenticated user.
    The user is identified by the token provided in the Authorization header.
    """
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    user = await user_service.get_user_show(user_id=current_user.id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user
