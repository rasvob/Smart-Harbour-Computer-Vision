import logging
import cv2
import base64
import requests
import json
import logging
from time import perf_counter_ns
from src.rtsp_grabber import RTSPGrabber
from app_log import AppLogger
from src.settings import app_settings
from src.api import send_health_check, send_frame, login_to_api, send_boat_pass_data    
from src.models import LoginModel, TokenModel, fake_boat_data
import urllib3

logger = AppLogger(__name__, logging._nameToLevel[app_settings.LOG_LEVEL]).get_logger()
urllib3.disable_warnings()

def crop_frame_with_padding(frame, xtl, ytl, xbr, ybr, padding=5):
    ytl = max(0, ytl-padding)
    ybr = min(1080, ybr+padding)
    xtl = max(0, xtl-padding)
    xbr = min(1920, xbr+padding)
    return frame[int(ytl):int(ybr), int(xtl):int(xbr)]

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
        _, buffer = cv2.imencode('.jpg', sub_frame)
        data_cropped_image = {'image': base64.b64encode(buffer).decode('utf-8')}
        ocr_response = requests.post(ocr_endpoint, headers=headers, data=json.dumps(data_cropped_image), verify=False)
        logger.debug(f'OCR response: {ocr_response.text}')
    end = perf_counter_ns()
    diff = (end - start) / 1000000
    logger.debug(f'Frame yolo+ocr time: {diff} ms')

    return True

if __name__ == "__main__":
    # load_dotenv()
    logger.info('Starting the application')
    logger.debug(app_settings)

    logger.info(f'Camera ID: {app_settings.CAMERA_ID}')

    logger.info('Sending health check to YOLO')
    res = send_health_check(app_settings.YOLO_HEALTH_ENDPOINT)
    logger.info(res)

    logger.info('Sending health check to OCR')
    res = send_health_check(app_settings.OCR_HEALTH_ENDPOINT)
    logger.info(res)

    logger.info('Sending health check to REST API')
    res = send_health_check(app_settings.BACKEND_ENDPOINT_HEALTH)
    logger.info(res)

    credentials = LoginModel(username=app_settings.BACKEND_USERNAME, password=app_settings.BACKEND_PASSWORD)
    token = login_to_api(credentials, f'{app_settings.BACKEND_ENDPOINT_BASE}{app_settings.BACKEND_PATH_LOGIN}')

    if not token:
        logger.error('AUTH ERROR - Token not received')
        exit(1)

    # fake_data = fake_boat_data()
    # logger.debug(fake_data)
    # ret = send_boat_pass_data(fake_data, f'{app_settings.BACKEND_ENDPOINT_BASE}{app_settings.BACKEND_PATH_BOAT_PASS}', token)
    # logger.debug(ret)
    # exit(0)

    # grabber = RTSPGrabber(ip='', port=0, channel=0, user='', password='', camera_id=app_settings.CAMERA_ID, data_dir='/app/data/frames')
    # grabber.start_capture(lambda x: process_frame(x, app_settings.YOLO_API_KEY, app_settings.YOLO_ENDPOINT, app_settings.OCR_ENDPOINT), override_url=app_settings.RTSP_ENDPOINT)