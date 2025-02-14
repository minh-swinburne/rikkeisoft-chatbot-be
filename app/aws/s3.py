from botocore.exceptions import ClientError, NoCredentialsError
from app.core.settings import settings
from app.utils import parse_timedelta
from app.aws import get_client
from cachetools import TTLCache
from typing import IO, Union

client = get_client("s3")
bucket_name = settings.aws_s3_bucket

url_expiry = parse_timedelta(settings.aws_s3_url_expires_in).total_seconds()
presigned_url_cache = TTLCache(maxsize=1000, ttl=url_expiry - 10)


def generate_presigned_url(object_name: str):
    """Generate or retrieve a cached presigned URL for an S3 object."""
    if object_name in presigned_url_cache:
        print(f"🔗 Using cached presigned URL for {object_name}")
        return presigned_url_cache[object_name]

    try:
        response = client.head_object(Bucket=bucket_name, Key=object_name)
        file_name = response["Metadata"].get("filename")
        print(f"🔗 Generated presigned URL for {file_name}.")

        url = client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_name,
                "ResponseContentDisposition": f"attachment; filename={file_name}",
            },  # noqa
            ExpiresIn=url_expiry,
        )

        presigned_url_cache[object_name] = url  # Cache the URL
        return url
    except (ClientError, NoCredentialsError) as e:
        print(f"❌ S3 Presigned URL Error: {e}")
        return None


def get_file(object_name: str) -> bytes:
    """Download a file from the S3 bucket."""
    try:
        response = client.get_object(Bucket=bucket_name, Key=object_name)
        print("📥 Downloaded file from S3 successfully.")
        return response["Body"].read()
    except (ClientError, NoCredentialsError) as e:
        print(f"❌ S3 Download Error: {e}")
        raise e


def download_file(object_name: str, file: Union[IO[bytes], str]) -> bool:
    """Download a file from the S3 bucket."""
    try:
        if isinstance(file, str):
            client.download_file(bucket_name, object_name, file)
        else:
            client.download_fileobj(bucket_name, object_name, file)
        print("📥 Downloaded file from S3 successfully.")
        return True
    except (ClientError, NoCredentialsError) as e:
        print(f"❌ S3 Download Error: {e}")
        return False


def put_file(object_name: str, file_data: bytes, extra_args: dict = {}) -> bool:
    """Upload a file to the S3 bucket."""
    try:
        client.put_object(
            Bucket=bucket_name, Key=object_name, Body=file_data, **extra_args
        )
        print("📤 Uploaded file to S3 successfully.")
        return True
    except (ClientError, NoCredentialsError) as e:
        print(f"❌ S3 Upload Error: {e}")
        return False


def upload_file(
    object_name: str, file: Union[IO[bytes], str], extra_args: dict = None
) -> bool:
    """Uploads a file or file-like object to the S3 bucket."""
    try:
        if isinstance(file, str):
            client.upload_file(file, bucket_name, object_name, ExtraArgs=extra_args)
        else:
            client.upload_fileobj(
                file,
                bucket_name,
                object_name,
                ExtraArgs=extra_args,
            )
        print("📤 Uploaded file to S3 successfully.")
        return True
    except (ClientError, NoCredentialsError) as e:
        print(f"❌ S3 Upload Error: {e}")
        return False


def delete_file(object_name: str) -> bool:
    """Delete a file from the S3 bucket."""
    try:
        client.delete_object(Bucket=bucket_name, Key=object_name)
        print("🗑️ Deleted file from S3 successfully.")
        return True
    except (ClientError, NoCredentialsError) as e:
        print(f"❌ S3 Delete Error: {e}")
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
