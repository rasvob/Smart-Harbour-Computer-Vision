import os
from dotenv import load_dotenv
from ultralytics import YOLO
from config.config_loader import ConfigLoader
from app_log.app_logger import AppLogger

logger = AppLogger(__name__).get_logger()

if __name__ == "__main__":
    load_dotenv()
    config_path = os.environ.get("CONFIG_PATH")
    config_section = os.environ.get("CONFIG_SECTION")
    config = ConfigLoader(config_path, config_section)
    params = config.get_params()

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