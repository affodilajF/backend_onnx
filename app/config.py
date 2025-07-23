from dotenv import load_dotenv
import os

load_dotenv()

# URL_CAM = int(os.getenv("URL_CAM"))
URL_CAM = os.getenv("URL_CAM")

MODEL_PATH = os.getenv("MODEL_PATH")
NUM_THREADS = int(os.getenv("NUM_THREADS"))
MODEL_INPUT_SIZE = tuple(map(int, os.getenv("MODEL_INPUT_SIZE").split(",")))

TRACKER_IOU_THRESHOLD = float(os.getenv("TRACKER_IOU_THRESHOLD"))
TRACKER_MAX_AGE = int(os.getenv("TRACKER_MAX_AGE"))
CONFIDENCE_THRESHOLD_PERSON_DETECTOR = float(os.getenv("CONFIDENCE_THRESHOLD_PERSON_DETECTOR"))