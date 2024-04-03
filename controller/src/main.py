import os
import logging
import cv2
import base64
import requests
import json
import time
from tqdm import tqdm
from dotenv import load_dotenv
import urllib3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
urllib3.disable_warnings()

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
    headers = {'Content-Type': 'application/json'}

    if api_key:
        headers['x-api-key'] = api_key

    data = {'image': encoded_image}
    response = requests.post(endpoint, headers=headers, data=json.dumps(data), verify=False)
    return response.text

def send_health_check(endpoint, api_key):
    response = requests.get(endpoint, verify=False)
    return response.text

if __name__ == "__main__":
    load_dotenv()
    logger.info('Starting the application')
    env_keys = ['YOLO_ENDPOINT', 'OCR_ENDPOINT', 'YOLO_API_KEY', 'OCR_API_KEY', 'YOLO_HEALTH_ENDPOINT', 'OCR_HEALTH_ENDPOINT']
    params = {x: os.environ.get(x) for x in env_keys}
    logger.debug(params)

    logger.info('Sending health check to YOLO')
    res = send_health_check(params['YOLO_HEALTH_ENDPOINT'], params['YOLO_API_KEY'])
    logger.debug(res)

    logger.info('Sending health check to OCR')
    res = send_health_check(params['OCR_HEALTH_ENDPOINT'], params['OCR_API_KEY'])
    logger.debug(res)

