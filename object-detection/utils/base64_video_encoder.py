import cv2
import os
import base64
from dotenv import load_dotenv
from video_stream import VideoStream

if __name__ == "__main__":
    load_dotenv()
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