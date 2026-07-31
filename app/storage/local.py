import uuid

from pathlib import Path

from fastapi import UploadFile

from app.storage.base import BaseStorage


UPLOAD_DIR = Path("uploads/images")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


class LocalStorage(BaseStorage):

    async def upload(
        self,
        file: UploadFile,
    ):

        filename = file.filename or ""
        extension = Path(filename).suffix

        filename = f"{uuid.uuid4()}{extension}"

        filepath = UPLOAD_DIR / filename

        with open(filepath, "wb") as buffer:

            buffer.write(
                await file.read()
            )

        return str(filepath)