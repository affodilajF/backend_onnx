from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_handler import handle_stream_websocket

router = APIRouter()

@router.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await handle_stream_websocket(websocket)
