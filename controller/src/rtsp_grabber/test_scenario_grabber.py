import logging
from datetime import datetime, timedelta
from time import perf_counter_ns
from app_log import AppLogger
import os
import cv2
import numpy as np
import queue
from dataclasses import dataclass

logger = AppLogger(__name__, logging.DEBUG).get_logger()
TEST_SCENARIO_FOLDER_TEMPLATE_NAME = '/app/SmartHarbourIntegrationTest/Camera_{0}'

class TestScenarioGrabber:
    """
        This test scenarios serve for integration testing of the system.
        Videos from two folders are read and processed by the system at the same time to simulate real-time processing.
        This scenario simulate the real-world time processing of the system. Timestamps are used to synchronize the processing of the videos. These simulated timestamps are saved into the database.
    """
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
    
    def run(self, process_frame):
        """
            Read video streams from video files in two folders.
            For synchronization, timestamps are used. The frames are entered into the queue with the timestamp and processed aferwards.
        """
        camera_stream_buffer1 = CameraStreamBuffer(TEST_SCENARIO_FOLDER_TEMPLATE_NAME.format('01'), '01')
        camera_stream_buffer2 = CameraStreamBuffer(TEST_SCENARIO_FOLDER_TEMPLATE_NAME.format('02'), '02')

        while True:        
            peak_frame1 = camera_stream_buffer1.peek()
            peak_frame2 = camera_stream_buffer2.peek()

            if peak_frame1 is None or peak_frame2 is None:
                logger.debug("End of video files reached")
                break

            if peak_frame1.timestamp == peak_frame2.timestamp:
                # logger.debug(f"Processing frames with timestamp: {peak_frame1.timestamp}")
                frame1 = next(camera_stream_buffer1)
                frame2 = next(camera_stream_buffer2)
                process_frame(frame1.frame, frame1.timestamp, 1)
                process_frame(frame2.frame, frame2.timestamp, 2)
            elif peak_frame1.timestamp < peak_frame2.timestamp:
                # logger.debug(f"Processing frame camera1 with timestamp: {peak_frame1.timestamp}")
                frame1 = next(camera_stream_buffer1)
                process_frame(frame1.frame, frame1.timestamp, 1)
            elif peak_frame1.timestamp > peak_frame2.timestamp:
                # logger.debug(f"Processing frame camera2 with timestamp: {peak_frame2.timestamp}")
                frame2 = next(camera_stream_buffer2)
                process_frame(frame2.frame, frame2.timestamp, 2)

@dataclass
class FrameItem:
    frame: np.ndarray
    timestamp: datetime
    
class CameraStreamBuffer:
    def __init__(self, video_files_directory, camera_id): # 
        self.video_files_directory = video_files_directory
        self.video_files_queue = queue.Queue()
        for video_file in sorted(os.listdir(self.video_files_directory)):
            if "videodemo" not in video_file:
                self.video_files_queue.put(video_file)
        self.camera_id = camera_id
        self.cap = None
        self.next_frame_item = None
        self.current_timestamp = None
        self._load_next_frame()

    def __iter__(self):
        return self

    def __next__(self):
        if self.next_frame_item is None:
            self._load_next_frame()
            if self.next_frame_item is None:
                raise StopIteration
        current_frame = self.next_frame_item
        self._load_next_frame()
        return current_frame

    def _load_next_video(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        logger.debug(f'queue size: {self.video_files_queue.qsize()}')
        if not self.video_files_queue.empty():
            file = self.video_files_queue.get()
            video_file = os.path.join(self.video_files_directory, file)
            logger.debug(f"Loading video file: {video_file}")
            self.cap = cv2.VideoCapture(video_file)
            current_timestamp = file.split('_')[-1].split('.')[0]
            self.current_timestamp = datetime.strptime(current_timestamp, "%Y%m%dT%H%M%S")
            if not self.cap.isOpened():
                raise Exception(f"Cannot open video file: {video_file}")

    def _load_next_frame(self):
        if self.cap is None:
            self._load_next_video()
            if self.cap is None:
                self.next_frame_item = None
                return
        ret, frame = self.cap.read()
        if not ret:
            self._load_next_video()
            if self.cap is None:
                self.next_frame_item = None
            else:
                self._load_next_frame()
        else:
            self.next_frame_item = FrameItem(frame, self.current_timestamp)
            self.current_timestamp += timedelta(milliseconds=250)
    
    def peek(self):
        return self.next_frame_item

    def reset(self, new_video_files_directory):
        if self.cap:
            self.cap.release()
        self.video_files_directory = new_video_files_directory
        self.video_files_queue = queue.Queue()
        for video_file in os.listdir(self.video_files_directory):
            self.video_files_queue.put(video_file)
        self._load_next_frame()

    def _get_timestamp_from_filename(self, filename):
        timestamp_str = filename.split('_')[-1].split('.')[0]
        return datetime.strptime(timestamp_str, "%Y%m%dT%H%M%S")


