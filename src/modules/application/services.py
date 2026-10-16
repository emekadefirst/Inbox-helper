from src.modules.application.dtos import (
    CreateApplicationDTO,
    ApplicationObjectDTO,
    ImportReportDTO,
    PaginatedApplicationDTO,
)
from src.ETL.load import import_applications as load_applications
from src.modules.application.models import  ProcessingStatus
from src.modules.application.repository import ApplicationRepository
from src.modules.application.signals import schedule_application_screening
from src.modules.jd.repository import JDRepository

class ApplicationService:
    repo = ApplicationRepository()

    @classmethod
    async def import_applications(
        cls,
        content: bytes,
        filename: str,
    ) -> ImportReportDTO:
        report = await load_applications(
            content=content,
            filename=filename,
            repo=cls.repo,
            jobs_repo=JDRepository(),
        )
        for application_id in report.created_ids:
            schedule_application_screening(str(application_id))
        return report

    @classmethod
    async def apply(cls, data: CreateApplicationDTO) -> ApplicationObjectDTO:
        application = await cls.repo.create(**data.model_dump())
        result = await cls.repo.fetch(id=str(application.id), page_size=1)
        return result.data[0]

    @classmethod
    async def fetch(
        cls,
        id: str | None = None,
        search: str | None = None,
        job_id: str | None = None,
        processing_status: ProcessingStatus | None = None,
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