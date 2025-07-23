from app.services.tracker.bytetracker2.kalman_filter import KalmanFilter
from app.services.tracker.bytetracker2.matching import iou
import numpy as np

class STrack:
    def __init__(self, bbox, track_id):
        self.bbox = bbox
        self.track_id = track_id
        self.age = 0
        self.time_since_update = 0
        self.kf = KalmanFilter()
        self.mean, self.covariance = self.kf.initiate(self.to_xyah(bbox))

    def to_xyah(self, bbox):
        x1, y1, x2, y2 = bbox
        w = x2 - x1
        h = y2 - y1
        x = x1 + w / 2.
        y = y1 + h / 2.
        return np.array([x, y, w, h])

    def to_tlbr(self):
        x, y, w, h = self.mean[:4]
        x1 = x - w / 2.
        y1 = y - h / 2.
        x2 = x + w / 2.
        y2 = y + h / 2.
        return [x1, y1, x2, y2]

    def predict(self):
        self.mean, self.covariance = self.kf.predict(self.mean, self.covariance)
        self.age += 1
        self.time_since_update += 1

    def update(self, bbox):
        self.mean, self.covariance = self.kf.update(self.mean, self.covariance, self.to_xyah(bbox))
        self.bbox = bbox
        self.time_since_update = 0

class BYTETracker:
    def __init__(self, iou_threshold, max_age):
        self.iou_threshold = iou_threshold
        self.max_age = max_age
        self.tracks = []
        self.track_id_count = 0

    def update(self, detections):
        # Predict new positions of existing tracks
        for track in self.tracks:
            track.predict()

        updated_tracks = []
        unmatched_detections = []
        matched_ids = set()

        for det in detections:
            matched = False
            for track in self.tracks:
                if iou(track.to_tlbr(), det[:4]) > self.iou_threshold:
                    track.update(det[:4])
                    updated_tracks.append((track.to_tlbr(), track.track_id))
                    matched_ids.add(track.track_id)
                    matched = True
                    break
            if not matched:
                unmatched_detections.append(det[:4])

        # Remove old tracks
        self.tracks = [t for t in self.tracks if t.time_since_update < self.max_age]

        # Add new tracks for unmatched detections
        for det in unmatched_detections:
            new_track = STrack(det, self.track_id_count)
            self.tracks.append(new_track)
            updated_tracks.append((new_track.to_tlbr(), new_track.track_id))
            self.track_id_count += 1

        return updated_tracks
