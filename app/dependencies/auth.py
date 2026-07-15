from jose import JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import decode_token
from app.db.session import get_db
from app.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):

    try:
        payload = decode_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )

    repository = UserRepository(db)

    user = await repository.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user