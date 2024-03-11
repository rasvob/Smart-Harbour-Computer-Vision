from typing import List
from PIL import Image
from ultralytics import YOLO
from app_log.app_logger import AppLogger
from dto.detection_model import DetectionModel

logger = AppLogger(__name__).get_logger()

class YoloDetectorService:
    def __init__(self, model_path:str, video_width:int, device:int, classes:List[int]) -> None:
        self.video_width = video_width
        self.device = device
        self.classes = classes
        self.model = YOLO(model_path, task='detect')
        self.logger = AppLogger(__name__).get_logger()

    def detect(self, frame:Image) -> List[dict]:
        results = self.model(frame ,imgsz=self.video_width, save_txt=False, save_conf=False, save=False, classes=self.classes, device=self.device)
        boxes = [x.boxes.data.cpu().numpy() for x in results][0]
        res = DetectionModel(boats_detected=len(boxes), detection_boxes=boxes)
        return res