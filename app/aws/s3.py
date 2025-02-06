import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from app.core.settings import settings
from app.aws import get_client
from typing import IO


client = get_client("s3")
bucket_name = settings.aws_s3_bucket


def generate_presigned_url(object_name: str, expiration=3600):
    try:
        response = client.head_object(Bucket=bucket_name, Key=object_name)
        file_name = response["Metadata"].get("filename")
        print(f"Generating presigned URL for {file_name}...")

        return client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_name,
                "ResponseContentDisposition": f"attachment; filename={file_name}",
            },  # noqa
            ExpiresIn=expiration,
        )
    except (ClientError, NoCredentialsError) as e:
        print(f"S3 Presigned URL Error: {e}")
        return None


def upload_file(object_name: str, file_obj: IO[bytes], extra_args: dict = None) -> str:
    """Uploads a file to S3 with a unique filename if necessary."""
    try:
        # if not overwrite:
        #     object_name = get_unique_filename(object_name)
        client.upload_fileobj(
            file_obj,
            bucket_name,
            object_name,
            ExtraArgs=extra_args,
        )
        return object_name
    except (ClientError, NoCredentialsError) as e:
        print(f"S3 Upload Error: {e}")
        raise e


def delete_file(object_name: str) -> bool:
    """Delete a file from the S3 bucket."""
    try:
        client.delete_object(Bucket=bucket_name, Key=object_name)
        return True
    except (ClientError, NoCredentialsError) as e:
        print(f"S3 Delete Error: {e}")
        return False


def file_exists(object_name: str) -> bool:
    """Check if an object exists in the S3 bucket."""
    try:
        client.head_object(Bucket=bucket_name, Key=object_name)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False  # Object does not exist
        raise e  # Raise other unexpected errors


def get_unique_filename(object_name: str) -> str:
    """Generate a unique filename by appending a suffix if necessary."""
    if not file_exists(object_name):
        return object_name  # No conflict, use the original name

    base, ext = object_name.rsplit(".", 1) if "." in object_name else (object_name, "")
    counter = 1
    while file_exists(f"{base}_{counter}.{ext}" if ext else f"{base}_{counter}"):
        counter += 1

    return f"{base}_{counter}.{ext}" if ext else f"{base}_{counter}"
