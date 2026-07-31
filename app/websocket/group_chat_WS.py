from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager
from app.db.session import AsyncSessionLocal
from app.repositories.group_member import GroupMemberRepository
from app.repositories.group_message import GroupMessageRepository
from app.services.group_message import GroupMessageService
from app.core.websocket_auth import get_user_id_from_token
from app.websocket.group_pubsub import publish_group_message

router = APIRouter()


@router.websocket("/ws/groups/{group_id}")
async def group_chat(
    websocket: WebSocket,
    group_id: str,
):
    # 1. Authentication
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    user_id = await get_user_id_from_token(token)
    if user_id is None:
        await websocket.close(code=1008)
        return

    db = AsyncSessionLocal()

    try:
        # 2. Authorization Check
        group_member_repo = GroupMemberRepository(db)
        allowed = await group_member_repo.is_member(group_id=group_id, user_id=user_id)
        if not allowed:
            await websocket.close(code=1008)
            return

        message_service = GroupMessageService(GroupMessageRepository(db))

        # 3. Connect & Notify Join
        await manager.connect_group(
            group_id=group_id,
            user_id=user_id,
            websocket=websocket,
        )

        # Notify room that user joined (System Notification)
        await publish_group_message(
            group_id,
            {
                "type": "system",
                "message": f"User {user_id} joined the group",
            },
        )

        # 4. Message Loop
        while True:
            data = await websocket.receive_json()
            content = data.get("content")

            if not content:
                continue

            # Save to Database
            message = await message_service.send_message(
                group_id=group_id,
                sender_id=user_id,
                content=content,
            )

            payload = {
                "type": "group_message",
                "id": str(message.id),
                "group_id": str(message.group_id),
                "sender": str(message.sender_id),
                "content": message.content,
                "created_at": message.created_at.isoformat(),
            }

            # Broadcast via Redis Pub/Sub & Manager
            await publish_group_message(group_id, payload)
            await manager.broadcast_to_group(group_id, payload)

    except WebSocketDisconnect:
        # Expected Client Disconnect
        pass
    except Exception as e:
        print(f"WebSocket Exception: {e}")
    finally:
        # Guarantee connection cleanup and DB session closure
        manager.disconnect_group(group_id, user_id)
        
        await manager.broadcast_to_group(
            group_id,
            {
                "type": "system",
                "message": f"{user_id} left the group",
            },
        )
        await db.close()