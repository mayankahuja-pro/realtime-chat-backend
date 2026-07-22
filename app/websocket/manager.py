from fastapi import WebSocket
from typing import Dict
import json


class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()

        self.active_connections[user_id] = websocket

        print("=" * 50)
        print("Connected:", user_id)
        print("Manager ID:", id(self))
        print("Active Connections:", list(self.active_connections.keys()))
        print("=" * 50)

    def disconnect(self, user_id: str):
        print(f"Disconnecting: {user_id}")

        self.active_connections.pop(user_id, None)

        print("Remaining:", list(self.active_connections.keys()))

    async def send_to_user(self,user_id: str,message: dict):
        print("\n" + "*" * 70)
        print(f"📨 Trying to send message to: {user_id}")

        websocket = self.active_connections.get(user_id)

        if websocket is None:
            print("❌ WebSocket NOT FOUND")
            print("Connected Users:", list(self.active_connections.keys()))
            print("*" * 70)
            return

        print("✅ WebSocket Found")
        print("📤 Sending Message:")
        print(message)

        await websocket.send_json(message)

        print("✅ Message Sent Successfully")
        print("*" * 70)
        
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


manager = ConnectionManager()