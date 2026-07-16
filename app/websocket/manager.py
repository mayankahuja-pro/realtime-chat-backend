from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # key = user_id
        # value = websocket
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

    async def send_personal_message(
        self,
        user_id: str,
        message: str,
    ):
        websocket = self.active_connections.get(user_id)

        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for websocket in self.active_connections.values():
            await websocket.send_text(message)

    def get_online_users(self):
        return list(self.active_connections.keys())


manager = ConnectionManager()