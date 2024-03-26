import json
from typing import List, Dict
from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Security, status
from app_log import AppLogger

logger = AppLogger(__name__).get_logger()

class ApiKeyStore:
    def __init__(self, keys_filepath:str | None = '/app/auth/api_keys.json') -> None:
        self.keys_filepath = keys_filepath
        self.keys:dict = self.load_keys()
    
    def load_keys(self) -> List[Dict[str, str]]:
        try:
            with open(self.keys_filepath, 'r') as f:
                keys = json.load(f)
        except Exception as e:
            logger.exception(e)
            keys = {}
        return keys

    def is_valid_key(self, key:str) -> bool:
        for v in self.keys:
            if key == v['key']:
                return True
        return False

api_key_header = APIKeyHeader(name='x-api-key', auto_error=False)
key_store = ApiKeyStore()

def get_api_key(api_key: str = Security(api_key_header)) -> str:
    logger.debug(f"API Key: {api_key}")
    logger.debug(f"API Key Store: {key_store.keys}")
    logger.debug(f"Is Valid Key: {key_store.is_valid_key(api_key)}")
    if not key_store.is_valid_key(api_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return api_key
