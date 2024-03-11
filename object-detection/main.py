import os
import io
import logging
import base64
from fastapi import FastAPI, HTTPException
from PIL import Image
from app_log import AppLogger
from services import YoloDetectorService
from dto import ImageModel
from config import ConfigLoader
from contextlib import asynccontextmanager

logger = AppLogger(__name__, logging.DEBUG).get_logger()
app_services = {
    'YoloDetectorService': None,
    'ConfigLoader': None
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    config_path = os.environ.get("CONFIG_PATH")
    config_section = os.environ.get("CONFIG_SECTION")
    app_services["ConfigLoader"] = ConfigLoader(config_path, config_section)
    params = app_services["ConfigLoader"].get_params()
    app_services["YoloDetectorService"] = YoloDetectorService(params['yolo-model'], params['video-width'], params['device'], [8])
    yield
    # Clean up the ML models and release the resources

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Message": "Yolo Object Detection Service is running!"}

@app.post("/detect")
async def detect_objects(data: ImageModel):
    try:
        # Decode the base64 string
        image_data = base64.b64decode(data.image)
        # Convert the bytes to a PIL Image object
        image = Image.open(io.BytesIO(image_data))
        results = app_services["YoloDetectorService"].detect(image)
        return results
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail="Invalid base64 image data")