from fastapi import HTTPException, status

from db.models.user import User
from hashing import Hasher
from repositories.user_repository import UserRepository
from schemas.auth_schemas import CreateUserRequest, ShowUser


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
            last_name=saved_user.last_name,
            date_joined=saved_user.date_joined,
            is_active=saved_user.is_active,
            is_staff=saved_user.is_staff,
            auth0_sub=saved_user.auth0_sub
        )
