import asyncio
import base64
import cv2
from app.services.video_manager import video_stream_manager

async def handle_stream_websocket(websocket):
    await websocket.accept()
    try:
        while video_stream_manager.is_running():
            if not video_stream_manager.output_queue.empty():
                frame, tracks = video_stream_manager.output_queue.get()
                await websocket.send_text(encode_frame_to_base64(frame))
            else:
                await asyncio.sleep(0.01)
    except Exception as e:
        print(f"WebSocket closed: {e}")

def encode_frame_to_base64(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    return base64.b64encode(buffer).decode("utf-8")
