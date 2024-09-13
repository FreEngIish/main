from typing import Optional

from fastapi import HTTPException, status

from db.models.user import User
from hashing import Hasher
from repositories.user_repository import UserRepository
from schemas.user_schemas import CreateUserRequest, ShowUser, UpdateUserRequest


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, create_user_request: CreateUserRequest) -> ShowUser:
        """Creates a new user in the database after validation checks."""

        # Check for existing user by username
        existing_user = await self.user_repo.get_user_by_username(
            create_user_request.username
        ) or await self.user_repo.get_user_by_email(create_user_request.email)
        if existing_user:
            raise ValueError('Username or email already registered')

        # Create new user
        new_user = User(
            username=create_user_request.username,
            hashed_password=Hasher.get_password_hash(create_user_request.password),
            email=create_user_request.email,
        )

        # Save user to the database through repository
        saved_user = await self.user_repo.add_user_to_db(new_user)

        return ShowUser(
            id=saved_user.id,
            email=saved_user.email,
            username=saved_user.username,
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
        )

    async def get_user_show(self, user_id: int) -> Optional[ShowUser]:
        """Retrieves a user's details by ID and returns it as ShowUser."""
        user = await self.user_repo.get_user_by_id(user_id=user_id)
        if user is None:
            return None

        return ShowUser(
            id=user.id, email=user.email, username=user.username, first_name=user.first_name, last_name=user.last_name
        )

    async def update_user(self, user_id: int, update_data: UpdateUserRequest) -> ShowUser:
        """Updates an existing user in the database."""
        user = await self.user_repo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        user.first_name = update_data.first_name or user.first_name
        user.last_name = update_data.last_name or user.last_name

        if update_data.password:
            user.hashed_password = Hasher.get_password_hash(update_data.password)

        updated_user = await self.user_repo.update_user(user)

        return ShowUser(
            id=updated_user.id,
            email=updated_user.email,
            username=updated_user.username,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
        )

    async def delete_user(self, user_id: int):
        """Deletes a user from the database."""
        user = await self.user_repo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        await self.user_repo.delete_user(user)
