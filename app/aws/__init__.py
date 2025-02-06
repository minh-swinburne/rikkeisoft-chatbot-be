import boto3
from botocore.config import Config
from app.core.settings import settings

aws_config = Config(
    region_name=settings.aws_region,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)

def get_client(service_name):
    return boto3.client(service_name)
