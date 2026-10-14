from fastapi import File, HTTPException, Query, UploadFile
from src.common.base_router import base_router
from src.common.base_dto import ErrorResponseDTO
from src.modules.application.dtos import (
    ApplicationObjectDTO,
    CreateApplicationDTO,
    ImportReportDTO,
    PaginatedApplicationDTO,
)
from src.modules.application.services import ApplicationService
from src.modules.application.models import  ProcessingStatus


application_router = base_router("/applications", ["Applications"])

@application_router.post(
    path="",
    response_model=ApplicationObjectDTO,
    responses={400: {"model": ErrorResponseDTO}},
    status_code=201,
)
async def create_application(data: CreateApplicationDTO):
    return await ApplicationService.create(data)

@application_router.get(
    path="",
    response_model=PaginatedApplicationDTO,
    responses={400: {"model": ErrorResponseDTO}},
    status_code=200,
)
async def fetch_applications(
    id: str | None = Query(None, description="Filter by application ID"),
    search: str | None = Query(None, description="Search by title, description, or note to intelligence"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    processing_status: ProcessingStatus | None = Query(None, description="Filter by processing status"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page for pagination"),
):
    return await ApplicationService.fetch(id=id, search=search, processing_status=processing_status, page=page, page_size=page_size)

@application_router.post(
    path="/import",
    response_model=ImportReportDTO,
    responses={400: {"model": ErrorResponseDTO}},
    status_code=201,
)
async def import_applications(file: UploadFile = File(...)):
    try:
        return await ApplicationService.import_applications(
            content=await file.read(),
            filename=file.filename or "",
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error