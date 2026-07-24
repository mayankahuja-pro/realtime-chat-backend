from abc import ABC, abstractmethod
from fastapi import UploadFile


class BaseStorage(ABC):

    @abstractmethod
    async def upload(
        self,
        file: UploadFile,
    ) -> str:
        pass