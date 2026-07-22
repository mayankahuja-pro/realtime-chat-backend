from fastapi import WebSocket
from typing import Dict
import json


class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()

        self.active_connections[user_id] = websocket



    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)
 
    async def send_to_user(self,user_id: str,message: dict):
        websocket = self.active_connections.get(user_id)
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


manager = ConnectionManager()