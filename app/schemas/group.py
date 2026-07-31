from uuid import UUID
from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str


class GroupResponse(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }