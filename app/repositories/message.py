from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message

from sqlalchemy import or_, and_, select
 
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
        user1: str,
        user2: str,
        limit: int = 20,
        offset: int = 0,
    ):
        stmt = (
            select(Message)
            .where(
                or_(
                    and_(
                        Message.sender_id == user1,
                        Message.receiver_id == user2,
                    ),
                    and_(
                        Message.sender_id == user2,
                        Message.receiver_id == user1,
                    ),
                )
            )
            .order_by(Message.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(stmt)

        return result.scalars().all()   

#     async def mark_as_read(
#     receiver_id,
#     sender_id
# ):
#     ...
