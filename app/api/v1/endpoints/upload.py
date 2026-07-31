from fastapi import APIRouter, UploadFile, File

from app.core.file_validator import validate_image
from app.services.file_service import FileService

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

service = FileService()


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
):

    await validate_image(file)

    path = await service.save_image(file)

    return {
        "message": "Uploaded Successfully",
        "path": path,
    }