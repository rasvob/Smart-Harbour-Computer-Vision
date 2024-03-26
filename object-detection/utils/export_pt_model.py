import dotenv
import yaml
import os
import shutil
from dotenv import load_dotenv
from ultralytics import YOLO

if __name__ == '__main__':
    load_dotenv()
    params = {
        'yolo-model': os.environ.get("YOLO_MODEL"),
        'format': os.environ.get("OUTPUT_YOLO_FORMAT"),
        'video-width': int(os.environ.get("VIDEO_WIDTH")),
        'device': os.environ.get("DEVICE"),
        'export-model': os.environ.get("EXPORT_MODEL")
    }

    model = YOLO(params['yolo-model'], verbose=True)
    model.export(format=params['format'], imgsz=params['video-width'], half=True, simplify=True, device=params['device'])

    if os.path.exists(params['export-model']):
        os.remove(params['export-model'])

    src_path = params['yolo-model'].replace('.pt', '.engine')
    print(f"Moving {src_path} to {params['export-model']}")
    shutil.move(src_path, params['export-model'])