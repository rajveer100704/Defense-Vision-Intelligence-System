from fastapi import WebSocket
from typing import List
from utils.logger import get_logger

logger = get_logger()

class ConnectionManager:
    """
    Manages active WebSocket connections for real-time target broadcasting.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New dashboard client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Dashboard client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        """
        Broadcasts a JSON-serialized event to all connected clients.
        """
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                # Optionally remove broken connection
                pass

manager = ConnectionManager()
