from app.services.tracker.bytetracker.bytetrack import BYTETracker
from app.config import TRACKER_IOU_THRESHOLD, TRACKER_MAX_AGE

class TrackerFactory:
    @staticmethod
    def create_tracker():
        return BYTETracker(
            iou_threshold=TRACKER_IOU_THRESHOLD,
            max_age=TRACKER_MAX_AGE,
        )
