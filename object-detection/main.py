import os
from fastapi import FastAPI
from app_log import AppLogger
from services import YoloDetector
from config import load_config

logger = AppLogger(__name__).get_logger()
app = FastAPI()

config_path = os.environ.get("CONFIG_PATH")
config = load_config(config_path)
config_section = 'yolo-test-model-on-video'
params = config[config_section]
model = YoloDetector(params['yolo-model'], params['video-width'], params['device'], [8])

@app.get("/")
def read_root():
    return {"Hello": "World 2"}

# Add POST route which accept image and return the detected objects in JSON
# The image should be a base64 encoded string
@app.post("/detect")
def detect_objects(image:str):
    logger.info("Detecting objects")
    return model.detect(image)