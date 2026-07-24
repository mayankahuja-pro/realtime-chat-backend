import uuid
from pathlib import Path

from fastapi import UploadFile

from app.storage.base import BaseStorage
from app.core.s3 import s3_client
from app.core.config import settings


class S3Storage(BaseStorage):

    async def upload(
        self,
        file: UploadFile,
    ) -> str:

        upload_filename = file.filename or ""
        extension = Path(upload_filename).suffix

        filename = f"{uuid.uuid4()}{extension}"

        s3_client.upload_fileobj(
            file.file,
            settings.AWS_BUCKET_NAME,
            filename,
            ExtraArgs={
                "ContentType": file.content_type,
            },
        )

        return filename