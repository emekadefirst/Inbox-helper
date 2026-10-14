from fastapi import Query
from src.modules.jd.services import JDService
from src.common.base_router import base_router
from src.common.base_dto import ErrorResponseDTO
from src.modules.jd.dtos import JDObjectDTO, CreateJDDTO, PaginatedJDResponseDTO

jd_router = base_router("/jds", ["Job Descriptions"])

@jd_router.post(
    path="",
    response_model=JDObjectDTO,
    responses={400: {"model": ErrorResponseDTO}},
    status_code=201,
)
async def create_job_description(data: CreateJDDTO):
    return await JDService.create(data)

@jd_router.get(
    path="",
    response_model=PaginatedJDResponseDTO,
    responses={400: {"model": ErrorResponseDTO}},
    status_code=200,
)
async def fetch_job_descriptions(
    id: str | None = Query(None, description="Filter by job description ID"),
    search: str | None = Query(None, description="Search by title, description, or note to intelligence"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page for pagination"),
):
    return await JDService.fetch(id=id, search=search, page=page, page_size=page_size)

