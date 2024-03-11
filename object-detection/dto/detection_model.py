from pydantic import BaseModel
from typing import List

class DetectionModel(BaseModel):
    boats_detected: int
    detection_boxes: List[List[float]]
