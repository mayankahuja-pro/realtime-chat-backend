from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, message: Message):
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_conversation(
        self,
        user1,
        user2,
    ):
        stmt = (
            select(Message)
            .where(
                ((Message.sender_id == user1) &
                 (Message.receiver_id == user2))
                |
                ((Message.sender_id == user2) &
                 (Message.receiver_id == user1))
            )
            .order_by(Message.created_at.asc())
        )

        result = await self.db.execute(stmt)

        return result.scalars().all()