from pydantic import Field
from pydantic_settings  import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='OD_')
    yolo_model: str = Field(...)
    video_width: int = Field(..., gt=0)
    device: int = Field(..., ge=0)
    target_classes: list = Field(...,  min_items=1)