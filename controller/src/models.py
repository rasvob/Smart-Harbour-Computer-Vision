from pydantic import BaseModel
from datetime import datetime
from enum import Enum
import logging
from typing import Optional, List
from src.app_log import AppLogger
from src.settings import app_settings

logger = AppLogger(__name__, logging._nameToLevel[app_settings.LOG_LEVEL]).get_logger()

class BoatLengthEnum(str, Enum):
    pod_8m = "pod 8m"
    nad_8m = "nad 8m"

class LoginModel(BaseModel):
    username: str
    password: str

class TokenModel(BaseModel):
    access_token: str
    token_type: str

class BoatPassBase(BaseModel):
    camera_id: int
    timestamp: datetime
    image_filename: str
    raw_text: str | None = None
    detected_identifier: str | None = None
    boat_length: BoatLengthEnum | None = None

class BoundingBoxBase(BaseModel):
    left: float
    top: float
    right: float
    bottom: float
    confidence: float
    class_identifier: int

class OcrResultBase(BaseModel):
    left: float
    top: float
    right: float
    bottom: float
    text: str
    confidence: float

class BoundingBoxCreate(BoundingBoxBase):
    ocr_results: List[OcrResultBase]

class BoatPassCreate(BoatPassBase):
    bounding_boxes: List[BoundingBoxCreate]

class BoatPassCreate(BoatPassBase):
    bounding_boxes: List[BoundingBoxCreate]

def fake_boat_data():
    str_data = '{ \
    "camera_id": 0, \
    "timestamp": "2024-04-16T13:49:49.466000", \
    "image_filename": "None Name", \
    "raw_text": "API TEST", \
    "detected_identifier": "RAW STRING", \
    "boat_length": "pod 8m", \
    "bounding_boxes": [ \
      { \
        "left": 0, \
        "top": 0, \
        "right": 0, \
        "bottom": 0, \
        "confidence": 0, \
        "class_identifier": 0, \
        "ocr_results": [ \
          { \
            "left": 0, \
            "top": 0, \
            "right": 0, \
            "bottom": 0, \
            "text": "string", \
            "confidence": 0, \
          }, \
          { \
            "left": 0, \
            "top": 0, \
            "right": 3, \
            "bottom": 5, \
            "text": "string", \
            "confidence": 0, \
          } \
        ] \
      } \
    ] \
    }'
    data = BoatPassCreate.model_validate_json(str_data)
    return data
