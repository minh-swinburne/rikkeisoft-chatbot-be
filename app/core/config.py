from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env at startup
load_dotenv(override=True)


class Settings(BaseSettings):
    root_dir: Path = Path(__file__).resolve().parent.parent
    upload_dir: Path = Path(os.getenv("UPLOAD_DIR"))
    # app_env: str = os.getenv("APP_ENV", "production")
    # db_url: str = os.getenv("DB_URL")
    # model_backend: str = os.getenv("MODEL_BACKEND")


settings = Settings()
