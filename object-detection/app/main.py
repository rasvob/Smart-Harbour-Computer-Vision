import os
import io
import logging
import base64
from fastapi import FastAPI, HTTPException, APIRouter, Request
from PIL import Image
from app_log import AppLogger
from services import YoloDetectorService
from dto import ImageModel
from config import AppConfig
from contextlib import asynccontextmanager
from routers import api_v1_router

logger = AppLogger(__name__, logging.DEBUG).get_logger()
app_config = AppConfig()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug(app_config.model_dump())
    app.state.yolo_detector_service = YoloDetectorService(app_config.yolo_model, app_config.video_width, app_config.device, app_config.target_classes)
    app.state.yolo_detector_service.model_init()
    yield
    # Clean up the ML models and release the resources

app = FastAPI(lifespan=lifespan)
app.include_router(api_v1_router)

@app.get("/")
def read_root():
    return {"Message": "Yolo Object Detection Service is running!"}

@app.get("/health")
def health_check():
    return {"Status": "Healthy"}


