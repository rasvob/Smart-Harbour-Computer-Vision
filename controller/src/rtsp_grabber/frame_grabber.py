import logging
from datetime import datetime
from time import perf_counter_ns
from app_log import AppLogger
import os
import cv2

logger = AppLogger(__name__, logging.DEBUG).get_logger()

class RTSPGrabber:
    def __init__(self, ip:str, port:int, channel:int, user:str, password:str, camera_id:int=0, data_dir:str=None) -> None:
        self.ip = ip
        self.port = port
        self.channel = channel
        self.user = user
        self.password = password
        self.camera_id = camera_id
        self.data_dir = data_dir

    def create_rtsp_url(self) -> str:
        return f'rtsp://{self.user}:{self.password}@{self.ip}:{self.port}/Streaming/Channels/{self.channel}/'

    def process_frame_image_save(self, frame):
        if not self.data_dir:
            raise Exception("Property data_dir is not set, please set it before calling this method")

        date_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")
        path = os.path.join(self.data_dir, f"frame_{self.camera_id}_{date_time}.jpeg")
        ret = cv2.imwrite(path, frame)
        return ret

    def start_capture(self, process_frame, override_url:str=None) -> None:
        url = override_url if override_url else self.create_rtsp_url()
        cap = cv2.VideoCapture(url)

        if not cap.isOpened():
            raise Exception(f"Stream {url} couldn't be opened")

        w, h, fps = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(cv2.CAP_PROP_FPS)

        logger.info(f"Opened stream: {w}x{h}@{fps} fps")

        while(cap.isOpened()):
            start = perf_counter_ns()
            ret, frame = cap.read()
            if ret == True:
                frame_ok = process_frame(frame)
                if not frame_ok:
                    logger.error("Frame couldn't be processed")
                    return False
            else:
                logger.error("Frame couldn't be read")
                return False
            end  = perf_counter_ns()
            diff = (end - start) / 1000000
            logger.debug(f'Frame process time: {diff} ms')

        cap.release()
        return True

    def start_capture_to_jpeg(self):
        self.start_capture(self.process_frame_image_save)

    def start_capture_to_video(self):
        # writer_type = cv2.VideoWriter_fourcc(*"hvc1")
        # writer_type = cv2.VideoWriter_fourcc('M','J','P','G')
        writer_type = cv2.VideoWriter_fourcc('a','v','c','1')
        date_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")
        path = os.path.join(self.data_dir, f"vid_{date_time}.mkv")
        out = cv2.VideoWriter(path, writer_type, 15, (3840, 2160))
        self.start_capture(lambda x: self.process_frame_video_save(x, out))
        out.release()