import os
from dotenv import load_dotenv
from ultralytics import YOLO
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    load_dotenv('.env.local')
    params = {
        'yolo-model': os.environ.get("YOLO_MODEL"),
        'input-file': os.environ.get("INPUT_FILE"),
        'video-width': int(os.environ.get("VIDEO_WIDTH")),
        'device': os.environ.get("DEVICE")
    }

    model = YOLO(params['yolo-model'], task='detect')
    video_file = params['input-file']
    results = model(video_file, stream=True, imgsz=params['video-width'], save_txt=True, save_conf=True, save=False, classes=[8], device=params['device'])
    i = 0
    for x in results:
        output = x.boxes.data.cpu().numpy()
        i += 1
        if output.shape[0] > 1:
            logger.error(f"Boats detected: {len(output)}, i={i}")
        logger.info(output.shape)