from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.groupMessage import GroupMessage
from datetime import datetime, timezone
from uuid import UUID
from app.models.groupMessage import GroupMessage

 


class GroupMessageRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        group_id: UUID | str,
        sender_id: UUID | str,
        content: str,
    ) -> GroupMessage:
        
        # Cast to UUID if passed as string to prevent asyncpg driver errors
        group_id_obj = UUID(group_id) if isinstance(group_id, str) else group_id
        sender_id_obj = UUID(sender_id) if isinstance(sender_id, str) else sender_id

        message = GroupMessage(
            group_id=group_id_obj,
            sender_id=sender_id_obj,
            content=content,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),  # Naive UTC datetime
        )

        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)

        return message