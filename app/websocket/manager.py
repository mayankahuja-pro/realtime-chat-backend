from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(
        self,
        user_id: str,
        websocket: WebSocket,
    ):
        await websocket.accept()

        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def send_to_user(
        self,
        user_id: str,
        message: dict,
    ):
        websocket = self.active_connections.get(user_id)

        if websocket:
            await websocket.send_json(message)

    def is_online(self, user_id: str) -> bool:
        return user_id in self.active_connections

    async def broadcast(self, message: dict, exclude_user_id: str = None):
        for user_id in list(self.active_connections.keys()):
            if exclude_user_id and user_id == exclude_user_id:
                continue
            await self.send_to_user(user_id, message)


manager = ConnectionManager()