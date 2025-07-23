import time
from collections import deque
from functools import wraps

class MetricsLogger:
    def __init__(self):
        self.inference_times = deque(maxlen=100)
        self.latencies = deque(maxlen=100)
        self.throughput_counter = 0
        self.last_throughput_time = time.time()
        self.model_load_time_ms = None
        self.fps_frame_count = 0
        self.last_fps_time = time.time()
        self.fps = 0

    def log_inference(self, duration_ms):
        self.inference_times.append(duration_ms)
        self._update_fps()

    def log_latency(self, latency_ms):
        self.latencies.append(latency_ms)

    def _update_fps(self):
        self.fps_frame_count += 1
        now = time.time()
        if now - self.last_fps_time >= 1.0:
            self.fps = self.fps_frame_count / (now - self.last_fps_time)
            self.last_fps_time = now
            self.fps_frame_count = 0

    def log_throughput(self):
        self.throughput_counter += 1

    def get_metrics(self):
        return {
            "avg_inference_time_ms": sum(self.inference_times) / len(self.inference_times) if self.inference_times else 0,
            "avg_latency_ms": sum(self.latencies) / len(self.latencies) if self.latencies else 0,
            "fps": self.fps,
            "throughput_fps": self.throughput_counter / (time.time() - self.last_throughput_time + 1e-6),
            "model_loading_time_ms": self.model_load_time_ms or 0,
        }

    def set_model_loading_time(self, load_time_ms):
        self.model_load_time_ms = load_time_ms

metrics_logger = MetricsLogger()

import logging
logging.basicConfig(level=logging.INFO)
def log_inference_metrics(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        start_infer = time.perf_counter()
        result = func(*args, **kwargs)
        inference_time = (time.perf_counter() - start_infer) * 1000

        logging.info(f"[infer] Inference Time: {inference_time:.2f}")

        return result
    return wrapper

