import yaml
from app_log.app_logger import AppLogger

logger = AppLogger(__name__).get_logger()

def load_config(config_path):
    with open(config_path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            logger.error(exc)