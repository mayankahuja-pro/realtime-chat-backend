from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.group_repository import (
    GroupRepository,
    GroupMemberRepository,
)
from app.schemas.group import GroupCreate, GroupResponse
from app.services.group_service import GroupService

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("", response_model=GroupResponse)
async def create_group(
    payload: GroupCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = GroupRepository(db)
    group = await repository.create_group(payload.name)
    return group


@router.post("/{group_id}/join")
async def join_group(
    group_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = GroupMemberRepository(db)
    service = GroupService(repository)

    return await service.join_group(
        group_id=group_id,
        user_id=current_user.id,
    )