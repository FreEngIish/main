from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.user import User
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schemas import CreateUserRequest, ShowUser
from src.service.auth_service import AuthService


class UserService:
    def __init__(self, db: AsyncSession):
        self.db_session = db
        self.user_repository = UserRepository(db)
        self.auth_service = AuthService()

    async def create_user(self, create_user_request: CreateUserRequest) -> ShowUser:
        """Creates a new user in the database after validation checks."""

        # Check for existing user by username
        existing_user_by_username = await self.user_repository.get_user_by_username(
            create_user_request.username
        )
        if existing_user_by_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already registered'
            )

        # Check for existing user by email
        existing_user_by_email = await self.user_repository.get_user_by_email(
            create_user_request.email
        )
        if existing_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already registered'
            )

        # Create new user
        new_user = User(
            username=create_user_request.username,
            hashed_password=self.auth_service.bcrypt_context.hash(create_user_request.password),
            email=create_user_request.email
        )

        # Save user to the database through repository
        saved_user = await self.user_repository.add_user_to_db(new_user)

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
