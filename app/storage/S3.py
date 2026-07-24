from fastapi import UploadFile

from app.storage.base import BaseStorage


class S3Storage(BaseStorage):

    async def upload(
        self,
        file: UploadFile,
    ):

        raise NotImplementedError(
            "Will implement in AWS section"
        )