import asyncio
from fastapi import APIRouter, WebSocket
from fastapi.responses import StreamingResponse
from app.services.video_stream_multiprocess_ws import websocket_stream
from app.services.video_manager import video_stream_manager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import cv2
import base64
from app.services.video_manager import video_stream_manager

router = APIRouter()

@router.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()

    try:
        while video_stream_manager.is_running():
            if not video_stream_manager.output_queue.empty():
                frame, tracks = video_stream_manager.output_queue.get()

                # Convert to JPEG
                _, buffer = cv2.imencode(".jpg", frame)
                jpg_as_text = base64.b64encode(buffer).decode("utf-8")

                # Send as base64 image
                await websocket.send_text(jpg_as_text)
            else:
                await asyncio.sleep(0.01)  # prevent CPU spike

    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")


