import requests
import logging
import time
import base64
import json
from typing import Any, Callable
from src.settings import app_settings
from src.app_log import AppLogger
from src.models import BoatPassCreate, BoatPassCreatePayload, LoginModel, PreviewImagePayload, TokenModel
from pydantic import BaseModel

logger = AppLogger(__name__, logging._nameToLevel[app_settings.LOG_LEVEL]).get_logger()

times = []
def measure_time(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        global times
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        times.append((end - start) * 1000)
        logger.debug(f'Execution time: {(end - start) * 1000} ms')
        return result
    return wrapper

def send_health_check(endpoint:str) -> str:
    try:
        response = requests.get(endpoint, verify=False)
    except Exception as e:
        logger.error(f'Health check failed: {e}')
        return False
    return response.text

# @measure_time
def send_frame(image: Any, endpoint:str, api_key:str) -> str | None:
    encoded_image = base64.b64encode(image).decode('utf-8')
    headers = {'Content-Type': 'application/json'}

    if api_key:
        headers['x-api-key'] = api_key

    data = {'image': encoded_image}

    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(data), verify=False)
        return response.text
    except Exception as e:
        logger.error(f'Failed to send frame: {e}')
        return None

def login_to_api(credentials: LoginModel, endpoint: str) -> TokenModel | None:
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
    data = {'username': credentials.username, 'password': credentials.password}
    try:
        response = requests.post(endpoint, headers=headers, verify=False, data=data)
    except Exception as e:
        logger.error(f'Failed to login: {e}')
        return None
    
    if response.status_code != 200:
        logger.error(f'Login failed: {response.text}')
        return None

    return TokenModel(**response.json())

def send_payload_to_rest_api(data: BaseModel, endpoint:str, token: TokenModel, error_text:str) -> requests.Response | None:
    headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': f'{token.token_type} {token.access_token}', 'Accept': 'application/json'}
    try:
        response = requests.post(endpoint, headers=headers, verify=False, data=data.json().encode('utf-8'))
        return response
    except Exception as e:
        logger.error(f'{error_text}: {e}')
        return None

def send_boat_pass_data(data: BoatPassCreatePayload, endpoint:str, token: TokenModel) -> requests.Response | None:
    return send_payload_to_rest_api(data, endpoint, token, 'Failed to send boat pass data')
    # headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': f'{token.token_type} {token.access_token}', 'Accept': 'application/json'}
    # try:
    #     response = requests.post(endpoint, headers=headers, verify=False, data=data.json().encode('utf-8'))
    #     return response
    # except Exception as e:
    #     logger.error(f'Failed to send boat pass data: {e}')
    #     return None
    
def send_camera_preview(data: PreviewImagePayload, endpoint:str, token: TokenModel) -> requests.Response | None:
    return send_payload_to_rest_api(data, endpoint, token, 'Failed to send camera preview')
    # headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': f'{token.token_type} {token.access_token}', 'Accept': 'application/json'}
    # try:
    #     response = requests.post(endpoint, headers=headers, verify=False, data=data.json().encode('utf-8'))
    #     return response
    # except Exception as e:
    #     logger.error(f'Failed to send boat pass data: {e}')
    #     return None