import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from db.models.user import User
from dependencies import get_current_user, get_user_service
from schemas.user_schemas import CreateUserRequest, ShowUser, UpdateUserRequest
from services.user_services import UserService


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
    except ValueError as err:
        logger.error(f'Value error occurred: {err}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except IntegrityError as err:
        logger.error(f'Integrity error occurred: {err}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Database error')
    except Exception as e:
        logger.error(f'Unexpected error occurred: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='An unexpected error occurred')


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
    try:
        user = await user_service.get_user_show(user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Unexpected error occurred: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='An unexpected error occurred')
    return user


@router.put('/', response_model=ShowUser)
async def update_user(
    update_data: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> ShowUser:
    """
    Update the current user's information.
    """
    try:
        return await user_service.update_user(user_id=current_user.id, update_data=update_data)
    except ValueError as err:
        logger.error(f'Value error occurred: {err}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except Exception as e:
        logger.error(f'Unexpected error occurred: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='An unexpected error occurred')


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    current_user: User = Depends(get_current_user), user_service: UserService = Depends(get_user_service)
):
    """
    Delete the current user.
    """
    try:
        await user_service.delete_user(user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Unexpected error occurred: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='An unexpected error occurred')

    return {'detail': 'User deleted successfully'}
