import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class GroupMessage(Base):
    __tablename__ = "group_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("groups.id")
    )

    sender_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id")
    )

    content: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime]