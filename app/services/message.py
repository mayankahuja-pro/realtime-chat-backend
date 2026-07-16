from app.models.message import Message
from app.repositories.message import MessageRepository


class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    async def save_private_message(
        self,
        sender_id,
        receiver_id,
        content,
    ):
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
        )

        return await self.repository.create(message)