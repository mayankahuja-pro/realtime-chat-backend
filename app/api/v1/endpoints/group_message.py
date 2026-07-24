from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.repositories.group_message import GroupMessageRepository
from app.services.group_message import GroupMessageService

router = APIRouter(prefix="/groups",tags=["Groups"])


@router.get("/{group_id}/messages")
async def get_group_messages(
    group_id: str,
    page: int = 1,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):

    service = GroupMessageService(
        GroupMessageRepository(db)
    )

    messages = await service.get_messages(
        group_id,
        page,
        limit,
    )

    return messages