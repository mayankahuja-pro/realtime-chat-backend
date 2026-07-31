import boto3

from app.core.config import settings


s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)

def generate_presigned_url(key: str) -> str:

    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.AWS_BUCKET_NAME,
            "Key": key,
        },
        ExpiresIn=3600,
    )