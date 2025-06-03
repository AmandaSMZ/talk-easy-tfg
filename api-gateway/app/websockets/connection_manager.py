from typing import Dict
from uuid import UUID
from fastapi import WebSocket

class ConnectionManager:

    active_connections: Dict[UUID, WebSocket]
    def __init__(self):
        self.active_connections = {}

    async def connect(self, user_id: UUID, websocket: WebSocket):
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: UUID):
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, message: dict, user_id: UUID):
        websocket = self.active_connections.get(user_id)
        print(f'Este es el mensaje : {message['text']}')
        if websocket:
            await websocket.send_json(message)
    
    def is_connected(self, user_id: UUID) -> bool:
        return user_id in self.active_connections

connection_manager = ConnectionManager()