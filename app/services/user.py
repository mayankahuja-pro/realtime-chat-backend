from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate

from app.core.auth import (
    create_access_token,
    create_refresh_token,
)
from app.core.security import verify_password
from app.schemas.auth import LoginRequest

class UserService:

    # initialize the repository
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    # sign up
    async def signup(self, user_data: UserCreate):

        existing = await self.repository.get_by_email(
            user_data.email
        )

        if existing:
            raise ValueError(
                "Email already registered"
            )

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password=hash_password(user_data.password),
        )

        return await self.repository.create_user(user)


    # login
    async def login(self, data: LoginRequest):
        user = await self.repository.get_by_email(
            data.email
        )

        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(
            data.password,
            user.password,
        ):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id)
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
