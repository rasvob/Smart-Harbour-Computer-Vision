from typing import List
from PIL import Image
from ultralytics import YOLO
from app_log.app_logger import AppLogger

class YoloDetectorService:
    def __init__(self, model_path:str, video_width:int, device:int, classes:List[int]) -> None:
        self.video_width = video_width
        self.device = device
        self.classes = classes
        self.model = YOLO(model_path, task='detect')
        self.logger = AppLogger(__name__).get_logger()

    def detect(self, frame:Image) -> List[dict]:
        results = self.model(frame ,imgsz=self.video_width, save_txt=False, save_conf=False, save=False, classes=self.classes, device=self.device)
        return results