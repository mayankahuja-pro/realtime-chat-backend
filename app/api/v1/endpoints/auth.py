from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=201,
)
async def signup(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):

    service = UserService(
        UserRepository(db)
    )

    try:
        return await service.signup(user)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )