from app.core.settings import settings
from app.aws import s3
import json
import os

FILE_NAME = "config.json"
OBJECT_NAME = os.path.join(settings.config_folder, FILE_NAME)

def load_config() -> dict:
    config_data = s3.get_file(OBJECT_NAME)
    return json.loads(config_data.decode("utf-8"))

def save_config(config):
    s3.put_file(OBJECT_NAME, json.dumps(config).encode("utf-8"))
