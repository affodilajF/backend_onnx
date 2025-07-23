from app.services.tracker.bytetracker.kalman_filter import KalmanFilter
from app.services.tracker.bytetracker.matching import iou
import numpy as np
import itertools


class STrack:
    _count = itertools.count()

    def __init__(self, bbox, min_hits=3):
        self.kalman_filter = KalmanFilter()
        self.mean, self.covariance = self.kalman_filter.initiate(self._to_xyah(bbox))
        self.track_id = next(self._count)

        self.hits = 1
        self.age = 1
        self.time_since_update = 0
        self.min_hits = min_hits
        self.confirmed = False

    def predict(self):
        self.mean, self.covariance = self.kalman_filter.predict(self.mean, self.covariance)
        self.age += 1
        self.time_since_update += 1

    def update(self, bbox):
        self.mean, self.covariance = self.kalman_filter.update(
            self.mean, self.covariance, self._to_xyah(bbox))
        self.hits += 1
        self.time_since_update = 0
        if self.hits >= self.min_hits:
            self.confirmed = True

    def to_tlbr(self):
        x, y, a, h = self.mean[:4]
        w = a * h
        x1 = x - w / 2
        y1 = y - h / 2
        x2 = x + w / 2
        y2 = y + h / 2
        return [x1, y1, x2, y2]

    def _to_xyah(self, bbox):
        x1, y1, x2, y2 = bbox
        w = x2 - x1
        h = y2 - y1
        x = x1 + w / 2.
        y = y1 + h / 2.
        a = w / float(h)
        return np.array([x, y, a, h])


class BYTETracker:
    def __init__(self, max_age=30, iou_threshold=0.5, min_hits=3):
        self.tracks = []
        self.max_age = max_age
        self.iou_threshold = iou_threshold
        self.min_hits = min_hits

    def update(self, detections):
        # Step 1: Predict all tracks
        for track in self.tracks:
            track.predict()

        # Step 2: Match detections to existing tracks
        matched_ids = set()
        used_track_ids = set()
        updated_tracks = []
        unmatched_detections = []

        for det in detections:
            matched = False
            for track in self.tracks:
                if track.track_id in used_track_ids:
                    continue
                iou_score = iou(track.to_tlbr(), det[:4])
                if iou_score > self.iou_threshold:
                    track.update(det[:4])
                    if track.confirmed:
                        updated_tracks.append((track.to_tlbr(), track.track_id))
                        matched_ids.add(track.track_id)
                    used_track_ids.add(track.track_id)
                    matched = True
                    break
            if not matched:
                unmatched_detections.append(det[:4])

        # Step 3: Initialize new tracks
        for det in unmatched_detections:
            track = STrack(det, self.min_hits)
            self.tracks.append(track)

        # Step 4: Remove old tracks
        self.tracks = [t for t in self.tracks if t.time_since_update < self.max_age]

        return updated_tracks
