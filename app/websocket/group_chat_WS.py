from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.manager import manager

from app.db.session import AsyncSessionLocal
from app.repositories.group_message import GroupMessageRepository
from app.services.group_message import GroupMessageService

router = APIRouter()


@router.websocket("/ws/groups/{group_id}/{user_id}")
async def group_chat(
    websocket: WebSocket,
    group_id: str,
    user_id: str,
):
    # Create DB Session
    db = AsyncSessionLocal()

    # Create Service
    service = GroupMessageService(
        GroupMessageRepository(db)
    )

    # Connect User
    await manager.connect_group(
        group_id=group_id,
        user_id=user_id,
        websocket=websocket,
    )

    # Notify Group
    await manager.broadcast_to_group(
        group_id,
        {
            "type": "system",
            "message": f"{user_id} joined the group",
        },
    )

    try:

        while True:

            data = await websocket.receive_json()

            # Save Message
            message = await service.send_message(
                group_id=group_id,
                sender_id=user_id,
                content=data["content"],
            )

            # Broadcast Saved Message
            await manager.broadcast_to_group(
                group_id,
                {
                    "type": "group_message",
                    "id": str(message.id),
                    "group_id": str(message.group_id),
                    "sender": str(message.sender_id),
                    "content": message.content,
                    "created_at": message.created_at.isoformat(),
                },
            )

    except WebSocketDisconnect:

        manager.disconnect_group(
            group_id,
            user_id,
        )

        await manager.broadcast_to_group(
            group_id,
            {
                "type": "system",
                "message": f"{user_id} left the group",
            },
        )

    finally:
        await db.close()