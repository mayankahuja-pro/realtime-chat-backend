from fastapi import WebSocket
from typing import Dict


class ConnectionManager:

    def __init__(self):
        # Private Chat
        # {
        #     "user_id": websocket
        # }
        self.active_connections: Dict[str, WebSocket] = {}

        # Group Chat
        # {
        #     "group_id": {
        #         "user_id": websocket
        #     }
        # }
        self.group_connections: Dict[str, Dict[str, WebSocket]] = {}

    # =====================================================
    # PRIVATE CHAT
    # =====================================================

    async def connect(
        self,
        user_id: str,
        websocket: WebSocket,
    ):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(
        self,
        user_id: str,
    ):
        self.active_connections.pop(user_id, None)

    async def send_to_user(
        self,
        user_id: str,
        message: dict,
    ):
        websocket = self.active_connections.get(user_id)

        if websocket:
            await websocket.send_json(message)

    async def broadcast(
        self,
        message: dict,
    ):
        for websocket in self.active_connections.values():
            await websocket.send_json(message)

    def is_online(
        self,
        user_id: str,
    ) -> bool:
        return user_id in self.active_connections

    # =====================================================
    # GROUP CHAT
    # =====================================================

    async def connect_group(
        self,
        group_id: str,
        user_id: str,
        websocket: WebSocket,
    ):
        await websocket.accept()

        if group_id not in self.group_connections:
            self.group_connections[group_id] = {}

        self.group_connections[group_id][user_id] = websocket

        print(f"\nUser {user_id} joined group {group_id}")
        print(self.group_connections)

    def disconnect_group(
        self,
        group_id: str,
        user_id: str,
    ):
        if group_id not in self.group_connections:
            return

        self.group_connections[group_id].pop(user_id, None)

        # Remove empty group
        if not self.group_connections[group_id]:
            del self.group_connections[group_id]

        print(f"\nUser {user_id} left group {group_id}")
        print(self.group_connections)

    async def broadcast_to_group(
        self,
        group_id: str,
        message: dict,
    ):
        if group_id not in self.group_connections:
            return

        dead_connections = []

        for user_id, websocket in self.group_connections[group_id].items():
            try:
                await websocket.send_json(message)
            except Exception:
                # Client disconnected unexpectedly
                dead_connections.append(user_id)

        # Cleanup dead connections
        for user_id in dead_connections:
            self.disconnect_group(group_id, user_id)

    def get_group_members(
        self,
        group_id: str,
    ):
        return list(
            self.group_connections.get(group_id, {}).keys()
        )


manager = ConnectionManager()