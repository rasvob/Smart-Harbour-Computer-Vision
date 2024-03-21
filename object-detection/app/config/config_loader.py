import yaml
from app_log.app_logger import AppLogger

logger = AppLogger(__name__).get_logger()

class ConfigLoader:
    def __init__(self, config_path:str, config_section:str) -> None:
        self.config_path = config_path
        self.config_section = config_section
        self.config = self.load_config()

    def load_config(self) -> None:
        with open(self.config_path, "r") as stream:
            try:
                config = yaml.safe_load(stream)
                return config
            except yaml.YAMLError as exc:
                logger.error(exc)
                raise exc
    
    def get_params(self, config_section:str=None) -> None:
        if config_section is None:
            config_section = self.config_section
        return self.config[config_section]