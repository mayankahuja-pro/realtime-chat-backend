import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.message import MessageRepository
from app.services.message import MessageService
from app.websocket.manager import manager
from app.websocket.redis_pubsub import publish

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
):

 

    await manager.connect(user_id, websocket)

    # Broadcast presence (online) status to other users
    await publish(
        {
            "type": "presence",
            "user_id": user_id,
            "status": "online"
        },
        exclude_user_id=user_id
    )

    db: AsyncSession = AsyncSessionLocal()

    service = MessageService(
        MessageRepository(db)
    )

    try:

        while True:

            text = await websocket.receive_text()

            try:
                payload = json.loads(text)

            except json.JSONDecodeError:

                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Invalid JSON format"
                    }
                )

                continue

            message_type = payload.get("type")

            if message_type == "ping":

                await websocket.send_json(
                    {
                        "type": "pong"
                    }
                )

                continue

            if message_type == "typing":

                await publish(
                    {
                        "type": "typing",
                        "sender_id": user_id,
                        "receiver_id": payload["receiver_id"]
                    }
                )

                continue

            if message_type != "message":

                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Unknown message type"
                    }
                )

                continue

            receiver_id = payload["receiver_id"]

            content = payload["content"]

            message = await service.save_private_message(
                sender_id=user_id,
                receiver_id=receiver_id,
                content=content,
            )

            response = {
                "type": "message",
                "id": str(message.id),
                "sender_id": str(message.sender_id),
                "receiver_id": str(message.receiver_id),
                "content": message.content,
                "is_read": message.is_read,
                "created_at": message.created_at.isoformat(),
            }

            await publish(response)

    except WebSocketDisconnect:

        print(f"{user_id} disconnected")

 
    finally:
        manager.disconnect(user_id)
        await db.close()

        # Broadcast presence (offline) status to other users
        await publish(
            {
                "type": "presence",
                "user_id": user_id,
                "status": "offline"
            },
            exclude_user_id=user_id
        )
