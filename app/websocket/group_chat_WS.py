from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager

router = APIRouter()


@router.websocket("/ws/groups/{group_id}/{user_id}")
async def group_chat(
    websocket: WebSocket,
    group_id: str,
    user_id: str,
):
    # Connect user to group
    await manager.connect_group(
        group_id=group_id,
        user_id=user_id,
        websocket=websocket,
    )

    # Notify everyone that a new user joined
    await manager.broadcast_to_group(
        group_id,
        {
            "type": "system",
            "message": f"{user_id} joined the group"
        },
    )

    try:

        while True:

            data = await websocket.receive_json()

            await manager.broadcast_to_group(
                group_id,
                {
                    "type": "group_message",
                    "sender": user_id,
                    "group_id": group_id,
                    "content": data["content"],
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
                "message": f"{user_id} left the group"
            },
        )