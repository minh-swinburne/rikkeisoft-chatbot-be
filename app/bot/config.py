from app.core.settings import settings
from app.utils import parse_timedelta
from app.aws import s3
from cachetools import TTLCache
import json
import os

FILE_NAME = "config.json"
OBJECT_NAME = os.path.join(settings.config_folder, FILE_NAME)

# Cache the config for 10 minutes
cache_expiry = parse_timedelta(settings.config_cache_expires_in)
config_cache = TTLCache(maxsize=1, ttl=cache_expiry.total_seconds())

def load_config(refresh: bool = False) -> dict:
    """Load config from cache or S3 if expired."""
    if not refresh and OBJECT_NAME in config_cache:
        print("🔗 Using cached config")
        return config_cache[OBJECT_NAME]  # Return cached config
    config_data = s3.get_file(OBJECT_NAME)
    config = json.loads(config_data.decode("utf-8"))
    config_cache[OBJECT_NAME] = config  # Cache the config
    print("🔗 Loaded config from S3")
    return config

def save_config(config):
    s3.put_file(OBJECT_NAME, json.dumps(config).encode("utf-8"))
    config_cache[OBJECT_NAME] = config  # Update the cache
    print("🔗 Saved config to S3")
