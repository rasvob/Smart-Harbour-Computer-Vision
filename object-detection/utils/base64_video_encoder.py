import cv2
import os
import base64
from dotenv import load_dotenv

class VideoStream():
    def __init__(self, video_name:str):
        self.video_name = video_name
        self.cap = cv2.VideoCapture(self.video_name)
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

if __name__ == "__main__":
    load_dotenv('.env.local')
    params = {
        'yolo-model': os.environ.get("YOLO_MODEL"),
        'input-file': os.environ.get("INPUT_FILE"),
        'video-width': int(os.environ.get("VIDEO_WIDTH")),
        'device': os.environ.get("DEVICE")
    }

    video = VideoStream(params['input-file'])
    limit = 1205
    # 0 boats at 0, 1 boat at 1164, 2 boats at 1205
    with open('base64frames_two.txt', 'wt') as f:
        for i, frame in enumerate(video):
            if i == limit:
                ret, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer)
                f.write(jpg_as_text.decode('utf-8'))
                break
            if i % 100 == 0:
                print(f"Processing frame {i}")