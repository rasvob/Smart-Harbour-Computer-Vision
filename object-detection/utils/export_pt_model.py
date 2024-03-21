import dotenv
import yaml
import os
from dotenv import load_dotenv
from ultralytics import YOLO

if __name__ == '__main__':
    load_dotenv()
    params = {
        'yolo-model': os.environ.get("YOLO_MODEL"),
        'format': os.environ.get("OUTPUT_YOLO_FORMAT"),
        'input-file': os.environ.get("INPUT_FILE"),
        'video-width': int(os.environ.get("VIDEO_WIDTH")),
        'device': os.environ.get("DEVICE")
    }

    model = YOLO(params['yolo-model'], verbose=True)
    model.export(format=params['format'], imgsz=params['video-width'], half=True, simplify=True, device=params['device'])