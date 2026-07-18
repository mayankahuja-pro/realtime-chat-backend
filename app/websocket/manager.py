from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # Stores active user connections
        # {user_id: websocket}
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(
        self,
        user_id: str,
        websocket: WebSocket,
    ):
        # Accept WebSocket connection
        await websocket.accept()

        # Save user's websocket
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        # Remove disconnected user
        self.active_connections.pop(user_id, None)

    async def send_personal_message(
        self,
        user_id: str,
        message: str,
    ):
        # Get user's websocket
        websocket = self.active_connections.get(user_id)

        # Send message if user is online
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        # Send message to all users
        for websocket in self.active_connections.values():
            await websocket.send_text(message)

    def get_online_users(self):
        # Return online user IDs
        return list(self.active_connections.keys())


# Global connection manager
manager = ConnectionManager()