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

logger = AppLogger(__name__, logging.DEBUG).get_logger()
api_v1_router = APIRouter(
    prefix="/api/v1",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

@api_v1_router.post("/detect")
async def detect_objects(data: ImageModel, request: Request):
    try:
        # Decode the base64 string
        image_data = base64.b64decode(data.image)
        # Convert the bytes to a PIL Image object
        image = Image.open(io.BytesIO(image_data))
        results = request.app.state.yolo_detector_service.detect(image)
        return results
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail="Invalid base64 image data")