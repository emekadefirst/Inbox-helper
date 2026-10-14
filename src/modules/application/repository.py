from src.common.base_repo import BaseRepository
from src.modules.application.models import Application, ProcessingStatus
from src.modules.application.dtos import (
    ApplicationObjectDTO,
    PaginatedApplicationDTO,
)
from tortoise.expressions import Q


class ApplicationRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Application)

    async def fetch(
        self,
        id: str | None = None,
        search: str | None = None,
        job_id: str | None = None,
        processing_status: ProcessingStatus | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedApplicationDTO:
        if page < 1 or page_size < 1:
            raise ValueError("page and page_size must be at least 1")

        query = Q()
        if id is not None:
            query &= Q(id=id)
        if search is not None:
            query &= (
                Q(from_email__icontains=search)
                | Q(candidate_name__icontains=search)
                | Q(subject__icontains=search)
                | Q(message__icontains=search)
            )
        if job_id is not None:
            query &= Q(job_id=job_id)
        if processing_status is not None:
            query &= Q(processing_status=processing_status)

        total = await self.model.filter(query).count()
        applications = await (
            self.model.filter(query)
            .select_related("job")
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        return PaginatedApplicationDTO(
            page=page,
            page_size=page_size,
            total=total,
            data=[
                ApplicationObjectDTO.model_validate(
                    application, from_attributes=True
                )
                for application in applications
            ],
        )