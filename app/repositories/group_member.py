from sqlalchemy import select

from app.models.groupMember import GroupMember


class GroupMemberRepository:

    def __init__(self, db):
        self.db = db

    async def is_member(
        self,
        group_id,
        user_id,
    ):

        stmt = select(GroupMember).where(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id,
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none() is not None