from app.repositories.group_message import GroupMessageRepository


class GroupMessageService:

    def __init__(self, repository: GroupMessageRepository):
        self.repository = repository

    async def send_message(
        self,
        group_id: str,
        sender_id: str,
        content: str,
    ):
        return await self.repository.create(
            group_id,
            sender_id,
            content,
        )

    async def get_messages(
        self,
        group_id,
        page,
        limit,
    ):
        return await self.repository.get_messages(
            group_id,
            page,
            limit,
        )