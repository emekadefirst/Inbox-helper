from src.common.base_repo import BaseRepository
from src.modules.response.models import Response, ResponseStatus
from src.modules.response.dtos import PaginatedResponseDTO, ResponseObjectDTO
from tortoise.expressions import Q


class ResponseRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Response)

    async def fetch(
        self,
        id: str | None = None,
        search: str | None = None,
        application_id: str | None = None,
        status: ResponseStatus | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedResponseDTO:
        if page < 1 or page_size < 1:
            raise ValueError("page and page_size must be at least 1")

        query = Q()
        if id is not None:
            query &= Q(id=id)
        if search is not None:
            query &= (
                Q(generated_response__icontains=search)
                | Q(authored_response__icontains=search)
            )
        if application_id is not None:
            query &= Q(application_id=application_id)
        if status is not None:
            query &= Q(status=status)

        total = await self.model.filter(query).count()
        responses = await (
            self.model.filter(query)
            .select_related("application", "application__job")
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        return PaginatedResponseDTO(
            page=page,
            page_size=page_size,
            total=total,
            data=[
                ResponseObjectDTO.model_validate(response, from_attributes=True)
                for response in responses
            ],
        )