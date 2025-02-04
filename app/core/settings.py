from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env at startup
load_dotenv(override=True)


class Settings(BaseSettings):
    aws_s3_bucket: str
    avatar_folder: str
    upload_folder: str
    upload_max_size: int

    tesseract_cmd: str
    doc_preview_url: str

    embedding_model: str
    embedding_dimension: int

    groq_api_key: str
    openai_api_key: str

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_expires_in: str
    jwt_refresh_expires_in: str

    db_dialect: str
    db_driver: str
    db_driver_async: str
    db_username: str
    db_password: str
    db_host: str
    db_port: str
    db_database: str
    db_logging: bool

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str
    google_user_info_url: str

    microsoft_client_id: str
    microsoft_client_secret: str
    microsoft_redirect_uri: str
    microsoft_authority: str

    milvus_host: str
    milvus_port: str
    milvus_db: str
    milvus_uri: str
    milvus_token: str
    # milvus_user: str
    # milvus_password: str
    milvus_collection: str


settings = Settings()
