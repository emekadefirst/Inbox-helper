from fastapi import Query
from src.common.base_router import base_router
from src.modules.response.services import ResponseService
from src.modules.response.dtos import ResponseObjectDTO, CreateResponseDTO, PaginatedResponseDTO, UpdateResponseDTO
from src.common.base_dto import ErrorResponseDTO

response_router = base_router("/responses", ["Responses"])

@response_router.get(
    path="",
    response_model=PaginatedResponseDTO,
    responses={400: {"model": ErrorResponseDTO}},
    status_code=200,
)
async def fetch_responses(
    id: str | None = Query(None, description="Filter by response ID"),
    search: str | None = Query(None, description="Search by generated or authored response"),
    application_id: str | None = Query(None, description="Filter by application ID"),
    status: str | None = Query(None, description="Filter by response status"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page for pagination"),
):

    return await ResponseService.fetch(id=id, search=search, application_id=application_id, status=status, page=page, page_size=page_size)

@response_router.patch(
    path="/{id}", 
    response_model=ResponseObjectDTO,
    responses={400: {"model": ErrorResponseDTO}, 404: {"model": ErrorResponseDTO}},
    status_code=200,
)
async def update_response(id: str, data: UpdateResponseDTO):
    updated_response = await ResponseService.update(id=id, data=data)
    if updated_response is None:
        return ErrorResponseDTO(message="Response not found", status_code=404)
    return updated_response