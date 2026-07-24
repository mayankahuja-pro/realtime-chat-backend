import uuid
from pathlib import Path

from fastapi import UploadFile

UPLOAD_DIR = Path("uploads/images")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


class FileService:

    async def save_image(
        self,
        file: UploadFile,
    ):

        extension = Path(file.filename).suffix

        filename = (
            f"{uuid.uuid4()}{extension}"
        )

        filepath = UPLOAD_DIR / filename

        with open(filepath, "wb") as buffer:
            buffer.write(
                await file.read()
            )

        return str(filepath)