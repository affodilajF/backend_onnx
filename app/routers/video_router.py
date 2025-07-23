from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.video_stream_multiprocess import generate_frames

router = APIRouter()

@router.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


