from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional
from pathlib import Path
import os

# Load .env at startup
load_dotenv(override=True)


class Settings(BaseSettings):
    root_dir: Path = Path(__file__).resolve().parent.parent
    upload_dir: Optional[Path] = Path(os.getenv("UPLOAD_DIR"))
    tesseract_cmd: str = os.getenv("TESSERACT_CMD")

    embedding_model: str = os.getenv("EMBEDDING_MODEL")
    embedding_dimension: int = os.getenv("EMBEDDING_DIMENSION")

    groq_api_key: str = os.getenv("GROQ_API_KEY")
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = os.getenv("GOOGLE_REDIRECT_URI")
    google_user_info_url: str = os.getenv("GOOGLE_USER_INFO_URL")

    microsoft_client_id: str = os.getenv("MICROSOFT_CLIENT_ID")
    microsoft_client_secret: str = os.getenv("MICROSOFT_CLIENT_SECRET")
    microsoft_redirect_uri: str = os.getenv("MICROSOFT_REDIRECT_URI")
    microsoft_authority: str = os.getenv("MICROSOFT_AUTHORITY")

    db_dialect: str = os.getenv("DB_DIALECT")
    db_driver: str = os.getenv("DB_DRIVER")
    db_username: str = os.getenv("DB_USERNAME")
    db_password: str = os.getenv("DB_PASSWORD")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")
    db_database: str = os.getenv("DB_DATABASE")

    milvus_host: str = os.getenv("MILVUS_HOST")
    milvus_port: str = os.getenv("MILVUS_PORT")
    milvus_db: str = os.getenv("MILVUS_DB")
    milvus_uri: str = os.getenv("MILVUS_URI")
    milvus_token: str = os.getenv("MILVUS_TOKEN")
    # milvus_user: str = os.getenv("MILVUS_USER")
    # milvus_password: str = os.getenv("MILVUS_PASSWORD")
    milvus_collection: str = os.getenv("MILVUS_COLLECTION")

    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM")
    jwt_access_expires_in: str = os.getenv("JWT_ACCESS_EXPIRES_IN")
    jwt_refresh_expires_in: str = os.getenv("JWT_REFRESH_EXPIRES_IN")


settings = Settings()
