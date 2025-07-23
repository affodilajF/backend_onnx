import time
from collections import defaultdict

class FPSLogger:
    def __init__(self, average_over=30):
        self.last_time = time.time()
        self.start_times = {}
        self.durations = defaultdict(list)
        self.frame_count = 0
        self.average_over = average_over
        self.total_fps_list = []

    def update(self):
        """Dipanggil setiap selesai 1 frame penuh (seluruh pipeline)"""
        now = time.time()
        delta = now - self.last_time
        self.last_time = now
        self.total_fps_list.append(1.0 / delta if delta > 0 else 0)
        self.frame_count += 1
        if len(self.total_fps_list) > self.average_over:
            self.total_fps_list.pop(0)

    def get_total_fps(self):
        if not self.total_fps_list:
            return 0
        return sum(self.total_fps_list) / len(self.total_fps_list)

    def start(self, name):
        """Mulai timer untuk pipeline tertentu"""
        self.start_times[name] = time.time()

    def stop(self, name):
        """Stop timer pipeline tertentu dan simpan durasinya"""
        if name in self.start_times:
            duration = time.time() - self.start_times[name]
            self.durations[name].append(duration)
            if len(self.durations[name]) > self.average_over:
                self.durations[name].pop(0)
            del self.start_times[name]

    def get_avg_duration(self, name):
        durs = self.durations.get(name, [])
        return sum(durs) / len(durs) if durs else 0

    def get_fps(self, name):
        avg_dur = self.get_avg_duration(name)
        return 1.0 / avg_dur if avg_dur > 0 else 0

    def log_all(self):
        print(f"[SYSTEM FPS] {self.get_total_fps():.2f}")
        for name in self.durations:
            print(f"  - {name} | avg: {self.get_avg_duration(name)*1000:.2f} ms | fps: {self.get_fps(name):.2f}")
