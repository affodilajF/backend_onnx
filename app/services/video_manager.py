import multiprocessing as mp
import cv2
from app.services.ai_inference.person_detector_multiprocess import infer, draw_boxes_with_ids
from app.services.tracker.tracker_factory import TrackerFactory

class VideoStreamManager:
    def __init__(self):
        self.input_queue = mp.Queue(maxsize=1)
        self.output_queue = mp.Queue(maxsize=1)
        self.process = None
        self.running = False

    def worker(self, input_q, output_q):
        cap = cv2.VideoCapture(0)
        tracker = TrackerFactory.create_tracker()

        while True:
            if not input_q.empty():
                stop_signal = input_q.get()
                if stop_signal is None:
                    break

            ret, frame = cap.read()
            if not ret:
                break

            detections = infer(frame)
            tracks = tracker.update(detections)
            frame = draw_boxes_with_ids(frame, tracks)

            if not output_q.full():
                output_q.put((frame, tracks))

        cap.release()

    def start(self):
        if self.running:
            return
        self.input_queue = mp.Queue(maxsize=1)
        self.output_queue = mp.Queue(maxsize=1)
        self.process = mp.Process(target=self.worker, args=(self.input_queue, self.output_queue))
        self.process.start()
        self.running = True

    def stop(self):
        if self.running and self.process is not None:
            try:
                self.input_queue.put_nowait(None)
            except:
                pass

            self.process.join(timeout=2)
            if self.process.is_alive():
                self.process.terminate()

            self.process = None
            self.running = False

    def is_running(self):
        return self.running

video_stream_manager = VideoStreamManager()
