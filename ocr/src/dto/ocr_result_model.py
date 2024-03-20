from pydantic import BaseModel
from typing import List, Tuple

class OCRResultModel(BaseModel):
    text: str
    ocr_recognitions: List[Tuple[List[List[int]], str, float]]
