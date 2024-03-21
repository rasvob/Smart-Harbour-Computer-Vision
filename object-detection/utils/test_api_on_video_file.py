import os
import logging
import cv2
import base64
import requests
from tqdm import tqdm
from dotenv import load_dotenv
from video_stream import VideoStream

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def send_frame(image, endpoint):
    encoded_image = base64.b64encode(image).decode('utf-8')
    headers = {'Content-Type': 'application/json'}
    data = {'image': encoded_image}
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    return response.text

if __name__ == "__main__":
    load_dotenv('.env.local')
    params = {
        'input-file': os.environ.get("INPUT_FILE"),
        'video-width': int(os.environ.get("VIDEO_WIDTH")),
    }

    video = VideoStream(params['input-file'])
    for i, frame in tqdm(enumerate(video)):
        ret, buffer = cv2.imencode('.jpg', frame)
        send_frame