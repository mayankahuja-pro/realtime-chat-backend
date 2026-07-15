from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

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