from src.modules.application.dtos import (
    CreateApplicationDTO,
    ApplicationObjectDTO,
    PaginatedApplicationDTO,
)
from src.modules.application.repository import ApplicationRepository

class ApplicationService:
    repo = ApplicationRepository()

    @classmethod
    async def apply(cls, data: CreateApplicationDTO) -> ApplicationObjectDTO:
        application = await cls.repo.create(data.dict())
        return ApplicationObjectDTO.model_validate(application, from_attributes=True)

    @classmethod
    async def fetch(
        cls,
        id: str | None = None,
        search: str | None = None,
        job_id: str | None = None,
        processing_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedApplicationDTO:
        return await cls.repo.fetch(
            id=id,
            search=search,
            job_id=job_id,
            processing_status=processing_status,
            page=page,
            page_size=page_size,
        )
    @classmethod
    async def get_by_id(cls, id: str) -> ApplicationObjectDTO | None:
        application = await cls.repo.get_by_id(id)
        if application is None:
            return None
        return ApplicationObjectDTO.model_validate(application, from_attributes=True)

    @classmethod
    async def update(cls, id: str, data: dict) -> ApplicationObjectDTO | None:
        application = await cls.repo.update(id, data)
        if application is None:
            return None
        return ApplicationObjectDTO.model_validate(application, from_attributes=True)

    @classmethod
    async def delete(cls, id: str) -> bool:
        return await cls.repo.delete(id)