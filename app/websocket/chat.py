import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.message import MessageRepository
from app.services.message import MessageService
from app.websocket.manager import manager

import json
router = APIRouter()

data = json.loads(await websocket.receive_text())

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
):
    await manager.connect(user_id, websocket)

    db: AsyncSession = AsyncSessionLocal()

    service = MessageService(
        MessageRepository(db)
    )

    try:
        while True:
            data = await websocket.receive_text()

            payload = json.loads(data)

            receiver_id = payload["receiver_id"]
            content = payload["content"]

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

        manager.disconnect(user_id)

    except Exception:

        manager.disconnect(user_id)

    finally:

        manager.disconnect(user_id)

    finally:
        await db.close()
    
        if data["type"]=="ping":

            await websocket.send_text(
                json.dumps(
                    {
                        "type":"pong"
                    }
                )
            )

            continue

    if data["type"] == "typing":

    await manager.send_personal_message(
        data["receiver_id"],
        json.dumps(
            {
                "type": "typing",
                "sender": user_id
            }
        )
    )

    continue