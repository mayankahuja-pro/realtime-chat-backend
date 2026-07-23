from sqlalchemy.ext.asyncio import AsyncSession

from app.models.group import Group

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.groupMember import GroupMember

class GroupRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_group(self, name: str) -> Group:
        group = Group(name=name)

        self.db.add(group)
        await self.db.commit()
        await self.db.refresh(group)

        return group




class GroupMemberRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def join_group(
        self,
        group_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> None:
        # Check if already a member
        stmt = select(GroupMember).where(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id,
        )
        result = await self.db.execute(stmt)
        member = result.scalar_one_or_none()

        if member:
            return

        member = GroupMember(
            group_id=group_id,
            user_id=user_id,
        )

        self.db.add(member)
        await self.db.commit()