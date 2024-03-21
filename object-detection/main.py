import os
import io
import logging
import base64
from fastapi import FastAPI, HTTPException
from PIL import Image
from app_log import AppLogger
from services import YoloDetectorService
from dto import ImageModel
from config import ConfigLoader, AppConfig
from contextlib import asynccontextmanager

logger = AppLogger(__name__, logging.DEBUG).get_logger()
app_config = AppConfig()

app_services = {
    'YoloDetectorService': None
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug(app_config.model_dump())
    app_services["YoloDetectorService"] = YoloDetectorService(app_config.yolo_model, app_config.video_width, app_config.device, app_config.target_classes)
    app_services["YoloDetectorService"].model_init()
    yield
    # Clean up the ML models and release the resources

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Message": "Yolo Object Detection Service is running!"}

@app.get("/health")
def health_check():
    return {"Status": "Healthy"}

@app.get("/config")
def get_config():
    return app_config.model_dump()

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