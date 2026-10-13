from uuid import UUID
from datetime import datetime
from src.common.base_dto import BaseDTO
from typing import Optional, List
from pydantic import BaseModel, Field
from src.modules.response.models import ResponseStatus
from src.modules.application.dtos import ApplicationNestedDTO


class CreateResponse(BaseModel):
    application_id: str = Field(..., max=60)
    classification: str = Field(..., max=100)
    classification_reason: Optional[str] = None 
    generated_response: str
    authored_response: str
    status: ResponseStatus = ResponseStatus.DRAFT

class ResponseObjectDTO(BaseDTO):
    application: ApplicationNestedDTO
    classification: str = Field(..., max=100)
    classification_reason: Optional[str] = None 
    generated_response: str
    authored_response: str
    status: ResponseStatus = ResponseStatus.DRAFT
    sent_at: Optional[str[datetime]] = None


class PaginatedResponseDTO(BaseModel):
    page: int = 1
    page: int = 10
    total: int
    data: List[ResponseObjectDTO]


