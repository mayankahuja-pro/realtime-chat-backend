from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.message import MessageRepository
from app.services.message import MessageService

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("/{user_id}")
async def get_messages(
    user_id: str,
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = MessageService(
        MessageRepository(db)
    )

    return await service.get_chat_history(
        str(current_user.id),
        user_id,
        limit,
        offset,
    )