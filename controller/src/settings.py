from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    YOLO_ENDPOINT:str
    YOLO_HEALTH_ENDPOINT:str
    OCR_ENDPOINT:str
    OCR_HEALTH_ENDPOINT:str
    # RTSP_ENDPOINT:str
    RTSP_IP:str
    RTSP_PORT:str
    RTSP_CHANNEL:str
    RTSP_USER:str
    RTSP_PASSWORD:str
    BACKEND_ENDPOINT_BASE:str
    BACKEND_PATH_LOGIN:str
    BACKEND_PATH_BOAT_PASS:str
    BACKEND_ENDPOINT_HEALTH:str
    BACKEND_PATH_PREVIEW: str
    CAMERA_ID:int
    YOLO_API_KEY:str
    OCR_API_KEY:str
    BACKEND_USERNAME:str
    BACKEND_PASSWORD:str
    LOG_LEVEL:str = 'INFO'

app_settings = Settings()