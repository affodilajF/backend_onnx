import cv2
import numpy as np
from app.config import MODEL_INPUT_SIZE, CONFIDENCE_THRESHOLD_PERSON_DETECTOR
from app.core.model_loader import ModelLoader
from app.utils.metrics_logger import log_inference_metrics

def preprocess(frame):
    img = cv2.resize(frame, MODEL_INPUT_SIZE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.normalize(img.astype(np.float32), None, alpha=0, beta=1.0, norm_type=cv2.NORM_MINMAX)
    img = np.transpose(img, (2, 0, 1))
    return np.expand_dims(img, axis=0)

@log_inference_metrics
def run_inference(model_loader, input_tensor):
    return model_loader.session.run(
        None, 
        {model_loader.input_name: input_tensor}
    )

def infer(frame):
    model_loader = ModelLoader.get_instance()
    input_tensor = preprocess(frame)
    preds = run_inference(model_loader, input_tensor)[0][0]

    detections = []
    for pred in preds:
        x1, y1, x2, y2, conf = pred[:5] 
        if conf >= CONFIDENCE_THRESHOLD_PERSON_DETECTOR:
            detections.append(np.array([x1, y1, x2, y2, conf]))

    return detections


def draw_boxes_with_ids(frame, tracked_objects):
    h, w = frame.shape[:2]
    scale_x = w / MODEL_INPUT_SIZE[0]
    scale_y = h / MODEL_INPUT_SIZE[1]

    for bbox, track_id in tracked_objects:
        x1, y1, x2, y2 = bbox
        x1, x2 = int(x1 * scale_x), int(x2 * scale_x)
        y1, y2 = int(y1 * scale_y), int(y2 * scale_y)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'ID: {track_id}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return frame

def get_color_for_id(track_id):
    np.random.seed(int(track_id) % 1000)
    return tuple(np.random.randint(64, 256, size=3).tolist()) 

