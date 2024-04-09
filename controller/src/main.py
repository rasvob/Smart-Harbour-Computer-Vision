import os
import logging
import cv2
import base64
import requests
import json
import time
import logging
from time import perf_counter_ns
from tqdm import tqdm
from dotenv import load_dotenv
from rtsp_grabber import RTSPGrabber
from app_log import AppLogger
import urllib3

logger = AppLogger(__name__, logging.DEBUG).get_logger()
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

def process_frame(frame, yolo_api_key, yolo_endpoint, ocr_endpoint):
    start = perf_counter_ns()
    ret, buffer = cv2.imencode('.jpeg', frame)
    end = perf_counter_ns()
    diff = (end - start) / 1000000
    logger.debug(f'Frame imencode time: {diff} ms')
    if not ret:
        logger.error('Frame couldn\'t be encoded')
        return False
    
    start = perf_counter_ns()
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    end = perf_counter_ns()
    diff = (end - start) / 1000000
    logger.debug(f'Frame b64encode time: {diff} ms')
    headers = {'Content-Type': 'application/json'}

    if yolo_api_key:
        headers['x-api-key'] = yolo_api_key

    data = {'image': encoded_image}

    start = perf_counter_ns()
    yolo_response = requests.post(yolo_endpoint, headers=headers, data=json.dumps(data), verify=False)
    logger.debug(f'YOLO response: {yolo_response.text}')
    yolo_response_json = json.loads(yolo_response.text)
    logger.debug(type(yolo_response_json['boats_detected']))
    if yolo_response_json['boats_detected'] > 0:
        sub_frame = crop_frame_with_padding(frame, yolo_response_json['detection_boxes'][0][0], yolo_response_json['detection_boxes'][0][1], yolo_response_json['detection_boxes'][0][2], yolo_response_json['detection_boxes'][0][3])
        retval, buffer = cv2.imencode('.jpg', sub_frame)
        data_cropped_image = {'image': base64.b64encode(buffer).decode('utf-8')}
        ocr_response = requests.post(ocr_endpoint, headers=headers, data=json.dumps(data_cropped_image), verify=False)
        logger.debug(f'OCR response: {ocr_response.text}')
    end = perf_counter_ns()
    diff = (end - start) / 1000000
    logger.debug(f'Frame yolo+ocr time: {diff} ms')

    return True

def crop_frame_with_padding(frame, xtl, ytl, xbr, ybr, padding=5):
    ytl = max(0, ytl-padding)
    ybr = min(1080, ybr+padding)
    xtl = max(0, xtl-padding)
    xbr = min(1920, xbr+padding)
    return frame[int(ytl):int(ybr), int(xtl):int(xbr)]

def send_health_check(endpoint, api_key):
    response = requests.get(endpoint, verify=False)
    return response.text

if __name__ == "__main__":
    # load_dotenv()
    logger.info('Starting the application')
    env_keys = ['YOLO_ENDPOINT', 'OCR_ENDPOINT', 'YOLO_API_KEY', 'OCR_API_KEY', 'YOLO_HEALTH_ENDPOINT', 'OCR_HEALTH_ENDPOINT', 'CAMERA_ID', 'RTSP_ENDPOINT']
    params = {x: os.environ.get(x) for x in env_keys}
    logger.debug(params)

    logger.info(f'Camera ID: {params["CAMERA_ID"]}')
    logger.info('Sending health check to YOLO')
    res = send_health_check(params['YOLO_HEALTH_ENDPOINT'], params['YOLO_API_KEY'])
    logger.debug(res)

    logger.info('Sending health check to OCR')
    res = send_health_check(params['OCR_HEALTH_ENDPOINT'], params['OCR_API_KEY'])
    logger.debug(res)

    grabber = RTSPGrabber(ip='', port=0, channel=0, user='', password='', camera_id=params['CAMERA_ID'], data_dir='/app/data/frames')
    grabber.start_capture(lambda x: process_frame(x, params['YOLO_API_KEY'], params['YOLO_ENDPOINT'], params['OCR_ENDPOINT']), override_url=params['RTSP_ENDPOINT'])