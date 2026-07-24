from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.manager import manager

from app.db.session import AsyncSessionLocal

from app.repositories.group_member import GroupMemberRepository
from app.repositories.group_message import GroupMessageRepository

from app.services.group_message import GroupMessageService

from app.core.websocket_auth import get_user_id_from_token

router = APIRouter()


@router.websocket("/ws/groups/{group_id}")
async def group_chat(
    websocket: WebSocket,
    group_id: str,
):
    # -----------------------------
    # Get JWT Token
    # -----------------------------
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return

    # -----------------------------
    # Verify JWT
    # -----------------------------
    user_id = await get_user_id_from_token(token)

    if user_id is None:
        await websocket.close(code=1008)
        return

    # -----------------------------
    # Create DB Session
    # -----------------------------
    db = AsyncSessionLocal()

    try:
        # -----------------------------
        # Check Group Membership
        # -----------------------------
        group_member_repo = GroupMemberRepository(db)

        allowed = await group_member_repo.is_member(
            group_id=group_id,
            user_id=user_id,
        )

        if not allowed:
            await websocket.close(code=1008)
            return

        # -----------------------------
        # Message Service
        # -----------------------------
        message_service = GroupMessageService(
            GroupMessageRepository(db)
        )

        # -----------------------------
        # Connect User
        # -----------------------------
        await manager.connect_group(
            group_id=group_id,
            user_id=user_id,
            websocket=websocket,
        )

        # Notify Everyone
        await manager.broadcast_to_group(
            group_id,
            {
                "type": "system",
                "message": f"{user_id}  joined the group",
            },
        )

        while True:

            data = await websocket.receive_json()

            content = data.get("content")

            if not content:
                continue

            # Save message
            message = await message_service.send_message(
                group_id=group_id,
                sender_id=user_id,
                content=content,
            )

            # Broadcast message
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

    except Exception as e:
        print("WebSocket Error:", e)

    finally:
        await db.close()