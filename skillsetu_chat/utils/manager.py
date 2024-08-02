import json

from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections."""

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(
                json.dumps({"type": "message", "data": message})
            )

    async def send_receipt_update(
        self, message_id: str, user_id: str, updated_status: str
    ):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(
                json.dumps(
                    {
                        "type": "receipt_update",
                        "data": json.dumps(
                            {"message_id": message_id, "status": updated_status}
                        ),
                    }
                )
            )

    async def is_connected(self, user_id: str):
        return user_id in self.active_connections


manager = ConnectionManager()
