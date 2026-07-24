from fastapi import UploadFile

from app.storage.local import LocalStorage


class FileService:

    def __init__(self):

        self.storage = LocalStorage()

    async def save_image(
        self,
        file: UploadFile,
    ):

        return await self.storage.upload(file)