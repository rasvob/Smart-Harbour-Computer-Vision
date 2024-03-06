import os
import dotenv
from ultralytics import YOLO
from config.config_loader import load_config
from app_log.app_logger import AppLogger

logger = AppLogger(__name__).get_logger()

if __name__ == "__main__":
    dotenv.load_dotenv()
    config_path = os.environ.get("CONFIG_PATH")
    config = load_config(config_path)

    config_section = 'yolo-test-model-on-video'
    params = config[config_section]
    

    model = YOLO(params['yolo-model'], task='detect')
    video_file = params['input-file']
    results = model(video_file, stream=True, imgsz=params['video-width'], save_txt=True, save_conf=True, save=False, classes=[8], device=0)

    for x in results:
        logger.info(x)