from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)


from app.dependencies.auth import get_current_user
from app.models.user import User

 
from fastapi.security import OAuth2PasswordRequestForm

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



@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(UserRepository(db))

    try:
        return await service.login(
            LoginRequest(
                email=form_data.username,   # username field contains email
                password=form_data.password,
            )
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )

@router.get(
    "/me",
    response_model=UserResponse,
)
async def me(
    current_user: User = Depends(get_current_user),
):
    return current_user