import requests
import logging
import time
import base64
import json
from src.settings import app_settings
from src.app_log import AppLogger
from src.models import BoatPassCreate, LoginModel, TokenModel

logger = AppLogger(__name__, logging._nameToLevel[app_settings.LOG_LEVEL]).get_logger()

times = []
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

def send_health_check(endpoint):
    try:
        response = requests.get(endpoint, verify=False)
    except Exception as e:
        logger.error(f'Health check failed: {e}')
        return False
    return response.text

# @measure_time
def send_frame(image, endpoint, api_key):
    encoded_image = base64.b64encode(image).decode('utf-8')
    headers = {'Content-Type': 'application/json'}

    if api_key:
        headers['x-api-key'] = api_key

    data = {'image': encoded_image}
    response = requests.post(endpoint, headers=headers, data=json.dumps(data), verify=False)
    return response.text

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

def send_boat_pass_data(data: BoatPassCreate, endpoint:str, token: TokenModel) -> str | None:
    headers = {'Content-Type': 'application/json', 'Authorization': f'{token.token_type} {token.access_token}', 'Accept': 'application/json'}
    try:
        response = requests.post(endpoint, headers=headers, verify=False, data=data.json())
        return response.text
    except Exception as e:
        logger.error(f'Failed to send boat pass data: {e}')
        return None