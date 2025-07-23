import cv2
import multiprocessing as mp
from app.services.AI.person_detector_multiprocess import infer, draw_boxes_with_ids
from app.config import URL_CAM
from app.utils.fps_logger import FPSLogger
from app.services.tracker.tracker_factory import TrackerFactory

# Setup video capture
cap = cv2.VideoCapture(0)

# Queue untuk komunikasi antar proses
input_queue = mp.Queue(maxsize=1)
output_queue = mp.Queue(maxsize=1)

def worker(input_q, output_q):
    tracker = TrackerFactory.create_tracker()
    fps_logger = FPSLogger()

    while True:
        frame = input_q.get()
        if frame is None:
            break  # keluar jika sinyal shutdown

        fps_logger.start("inference")
        detections = infer(frame)
        fps_logger.stop("inference")

        fps_logger.start("tracking")
        updated_tracks = tracker.update(detections)
        fps_logger.stop("tracking")

        output_q.put((frame, updated_tracks))

        fps_logger.update()
        # if fps_logger.frame_count % 30 == 0:
        #     print("[Worker FPS]")
        #     fps_logger.log_all()

def generate_frames():
    fps_logger = FPSLogger()

    process = mp.Process(target=worker, args=(input_queue, output_queue))
    process.start()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        if not input_queue.full():
            input_queue.put(frame.copy())

        if not output_queue.empty():
            result_frame, updated_tracks = output_queue.get()

            fps_logger.start("drawing")
            display = draw_boxes_with_ids(result_frame, updated_tracks)
            fps_logger.stop("drawing")

            fps_logger.start("encoding")
            ret, buffer = cv2.imencode('.jpg', display)
            fps_logger.stop("encoding")

            fps_logger.update()
            # if fps_logger.frame_count % 30 == 0:
            #     print("[Main Thread FPS]")
            #     fps_logger.log_all()

            frame_bytes = buffer.tobytes()
            # print("------------------------------")
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
