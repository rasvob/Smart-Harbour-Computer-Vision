import os
import logging
import cv2
import base64
import requests
import json
import time
from tqdm import tqdm
from dotenv import load_dotenv
from video_stream import VideoStream

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
times = []

# Create decorator for measuring time in miliseconds, store times in array and return average time
def measure_time(func):
    def wrapper(*args, **kwargs):
        global times
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        times.append((end - start) * 1000)
        logger.debug(f'Execution time: {(end - start) * 1000} ms')
        return result
    return wrapper

@measure_time
def send_frame(image, endpoint, api_key):
    encoded_image = base64.b64encode(image).decode('utf-8')
    headers = {'Content-Type': 'application/json', 'x-api-key': api_key}
    data = {'image': encoded_image}
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    return response.text

if __name__ == "__main__":
    load_dotenv()
    params = {
        'input-file': os.environ.get("INPUT_FILE"),
        'video-width': int(os.environ.get("VIDEO_WIDTH")),
        'api-endpoint': os.environ.get("ENDPOINT"),
        'api-key': os.environ.get("API_KEY"),
    }

    video = VideoStream(params['input-file'])
    for frame in tqdm(video, total=len(video)):
        ret, buffer = cv2.imencode('.jpg', frame)
        res = send_frame(buffer, params['api-endpoint'], params['api-key'])

    print(f'Average time: {sum(times) / len(times)} ms')