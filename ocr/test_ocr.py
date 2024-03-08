import requests
import json
import base64
import time

import cv2
import yaml
import os

class VideoStream():
    def __init__(self, video_name):
        self.video_name = video_name
        self.CAM = '01' if '_cam_01' in video_name else '02'
        self.folder = 'data_test'
        self.video_path = os.path.join(self.folder, self.video_name)
        self.cap = cv2.VideoCapture(self.video_path)
        self.frame_id = -1

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame_id += 1
            return frame
        else:
            raise StopIteration

    def __len__(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __getitem__(self, idx):
        for _ in range(idx - self.frame_id):
            ret, frame = self.cap.read()
        if ret:
            self.frame_id = idx
            return frame
        else:
            raise IndexError

    def __del__(self):
        self.cap.release()


def crop_frame(frame, xtl, ytl, xbr, ybr, padding=5):
    ytl = max(0, ytl-padding)
    ybr = min(1080, ybr+padding)
    xtl = max(0, xtl-padding)
    xbr = min(1920, xbr+padding)
    return frame[int(ytl):int(ybr), int(xtl):int(xbr)], (int(xtl), int(ytl))



def get_ocr_text(image):
    url = 'http://localhost:5000/serve'
    encoded_image = base64.b64encode(image).decode('utf-8')
    headers = {'Content-Type': 'application/json'}
    data = {'image': encoded_image}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.text


start_time = time.time()

video_name = 'cfg_raw_cam_02_fhd_h265_20230610T091000.mkv'
video_object = VideoStream(video_name)

for e, frame in enumerate(video_object):
    start_frame_time = time.time()
    frame = frame[:540,:960,:]
    retval, buffer = cv2.imencode('.jpg', frame)
    detected_text = get_ocr_text(buffer)
    print('detected_text', detected_text)
    print('Frame processing time:', time.time() - start_frame_time)

    if e > 100:
        break

print('Processing time:', time.time() - start_time)