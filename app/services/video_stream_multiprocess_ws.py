import cv2
import base64
import asyncio
import multiprocessing as mp
from fastapi import WebSocket
from app.services.AI.person_detector_multiprocess import infer, draw_boxes_with_ids
from app.services.tracker.tracker_factory import TrackerFactory

cap = cv2.VideoCapture(0)
input_queue = mp.Queue(maxsize=1)
output_queue = mp.Queue(maxsize=1)

def worker(input_q, output_q):
    tracker = TrackerFactory.create_tracker()
    while True:
        frame = input_q.get()
        if frame is None:
            break
        detections = infer(frame)
        tracks = tracker.update(detections)
        output_q.put((frame, tracks))

async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    process = mp.Process(target=worker, args=(input_queue, output_queue))
    process.start()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            if not input_queue.full():
                input_queue.put(frame)

            if not output_queue.empty():
                result_frame, tracks = output_queue.get()
                display = draw_boxes_with_ids(result_frame, tracks)

                _, buffer = cv2.imencode(".jpg", display)
                jpg_as_text = base64.b64encode(buffer).decode("utf-8")
                await websocket.send_text(jpg_as_text)

            await asyncio.sleep(0.03)  # ~30fps
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        input_queue.put(None)
        process.join()
        await websocket.close()
