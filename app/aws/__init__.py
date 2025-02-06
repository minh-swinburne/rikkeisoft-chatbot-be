import boto3
from botocore.config import Config

aws_config = Config(
    region_name="ap-southeast-2",
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)

def get_client(service_name):
    return boto3.client(service_name)
