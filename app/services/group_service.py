import uuid

from app.repositories.group_repository import GroupMemberRepository


class GroupService:
    def __init__(self, repository: GroupMemberRepository):
        self.repository = repository

    async def join_group(
        self,
        group_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        await self.repository.join_group(group_id, user_id)
        return {"message": "Joined successfully"}