import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.message import MessageRepository
from app.services.message import MessageService
from app.websocket.manager import manager

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
):
    await manager.connect(user_id, websocket)

    # Broadcast presence (online) status to other users
    await manager.broadcast(
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
            data = await websocket.receive_text()
            payload = json.loads(data)

            msg_type = payload.get("type")

            if msg_type == "ping":
                await websocket.send_json({"type": "pong"})
                continue

            elif msg_type == "typing":
                receiver_id = payload.get("receiver_id")
                if receiver_id:
                    await manager.send_to_user(
                        receiver_id,
                        {
                            "type": "typing",
                            "sender": user_id
                        }
                    )
                continue

            elif msg_type == "read_receipt":
                message_id = payload.get("message_id")
                if message_id:
                    updated_msg = await service.mark_message_as_read(message_id)
                    if updated_msg:
                        await manager.send_to_user(
                            str(updated_msg.sender_id),
                            {
                                "type": "read_receipt",
                                "message_id": message_id,
                                "reader_id": user_id
                            }
                        )
                continue

            else:
                receiver_id = payload.get("receiver_id")
                content = payload.get("content")

                if not receiver_id or not content:
                    continue

                message = await service.save_private_message(
                    sender_id=user_id,
                    receiver_id=receiver_id,
                    content=content,
                )

                response = {
                    "id": str(message.id),
                    "sender_id": str(message.sender_id),
                    "receiver_id": str(message.receiver_id),
                    "content": message.content,
                    "is_read": message.is_read,
                    "created_at": message.created_at.isoformat(),
                }

                await manager.send_to_user(
                    receiver_id,
                    response,
                )

                await manager.send_to_user(
                    user_id,
                    response,
                )

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        manager.disconnect(user_id)
        await db.close()

        # Broadcast presence (offline) status to other users
        await manager.broadcast(
            {
                "type": "presence",
                "user_id": user_id,
                "status": "offline"
            },
            exclude_user_id=user_id
        )