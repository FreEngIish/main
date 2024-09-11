from typing import Optional

from fastapi import HTTPException, status

from db.models.user import User
from hashing import Hasher
from repositories.user_repository import UserRepository
from schemas.user_schemas import CreateUserRequest, ShowUser


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    async def create_user(self, create_user_request: CreateUserRequest) -> ShowUser:
        """Creates a new user in the database after validation checks."""

        # Check for existing user by username
        existing_user = await self.user_repo.get_user_by_username(create_user_request.username) \
                        or await self.user_repo.get_user_by_email(create_user_request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username or email already registered'
            )

        # Create new user
        new_user = User(
            username=create_user_request.username,
            hashed_password=Hasher.get_password_hash(create_user_request.password),
            email=create_user_request.email
        )

        # Save user to the database through repository
        saved_user = await self.user_repo.add_user_to_db(new_user)

        return ShowUser(
            id=saved_user.id,
            email=saved_user.email,
            username=saved_user.username,
            first_name=saved_user.first_name,
            last_name=saved_user.last_name
        )

    async def get_user_show(self, user_id: int) -> Optional[ShowUser]:
        """Retrieves a user's details by ID and returns it as ShowUser."""
        user = await self.user_repo.get_user_by_id(user_id=user_id)
        if user is None:
            return None

        return ShowUser(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
