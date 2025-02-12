from cachetools import TTLCache
from app.core.settings import settings
from app.aws import s3
import json
import os

FILE_NAME = "config.json"
OBJECT_NAME = os.path.join(settings.config_folder, FILE_NAME)

# Cache the config for 10 minutes
config_cache = TTLCache(maxsize=1, ttl=10 * 60)

def load_config(refresh: bool = False) -> dict:
    """Load config from cache or S3 if expired."""
    if not refresh and OBJECT_NAME in config_cache:
        return config_cache[OBJECT_NAME]  # Return cached config
    config_data = s3.get_file(OBJECT_NAME)
    config = json.loads(config_data.decode("utf-8"))
    config_cache[OBJECT_NAME] = config  # Cache the config
    return config

def save_config(config):
    s3.put_file(OBJECT_NAME, json.dumps(config).encode("utf-8"))
