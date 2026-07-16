from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.manager import manager

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
):

    await manager.connect(user_id, websocket)

    await manager.broadcast(
        f"🟢 User {user_id} joined"
    )

    try:
        while True:
            message = await websocket.receive_text()

            await manager.broadcast(
                f"{user_id}: {message}"
            )

    except WebSocketDisconnect:

        manager.disconnect(user_id)

        await manager.broadcast(
            f"🔴 User {user_id} left"
        )