from app.storage.s3 import S3Storage
from app.core.s3 import generate_presigned_url


class FileService:

    def __init__(self):
        self.storage = S3Storage()

    async def save_image(self, file):

        key = await self.storage.upload(file)

        url = generate_presigned_url(key)

        return {
            "key": key,
            "url": url,
        }