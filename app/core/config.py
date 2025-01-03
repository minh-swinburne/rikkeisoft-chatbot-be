from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load .env at startup
load_dotenv()


class Settings(BaseSettings):
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")
    # app_env: str = os.getenv("APP_ENV", "production")
    # db_url: str = os.getenv("DB_URL")
    # model_backend: str = os.getenv("MODEL_BACKEND")


settings = Settings()
