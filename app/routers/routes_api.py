from fastapi import APIRouter, HTTPException
from app.core.system_state import system_state
from app.services.video_manager import video_stream_manager

router = APIRouter(prefix="/api")

@router.get("/sync")
async def get_sync():
    try:
        return system_state.get_all_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/start")
async def start_system():
    print("MASUK START")
    try:
        video_stream_manager.start()
        system_state.set_running("system_state", True)
        return {"message": "System started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
async def stop_system():
    print("MASUK STOP")
    try:
        video_stream_manager.stop()
        system_state.set_running("system_state", False)
        return {"message": "System stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


