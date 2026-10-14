from uuid import UUID
from datetime import datetime
from src.common.base_dto import BaseDTO
from typing import Optional, List
from pydantic import BaseModel, Field
from src.modules.response.models import ResponseStatus
from src.modules.application.dtos import ApplicationNestedDTO


class CreateResponseDTO(BaseModel):
    application_id: str = Field(..., max=60)
    classification: str = Field(..., max=100)
    classification_reason: Optional[str] = None 
    generated_response: str
    authored_response: str
    status: ResponseStatus = ResponseStatus.DRAFT

class UpdateResponseDTO(BaseModel):
    application_id: Optional[str] = Field(None, max=60)
    classification: Optional[str] = Field(None, max=100)
    classification_reason: Optional[str] = None 
    generated_response: Optional[str] = None
    authored_response: Optional[str] = None
    status: Optional[ResponseStatus] = None

class ResponseObjectDTO(BaseDTO):
    application: ApplicationNestedDTO
    classification: Optional[str] = Field(None, max=100)
    classification_reason: Optional[str] = None 
    generated_response: str
    authored_response: str
    status: ResponseStatus = ResponseStatus.DRAFT
    sent_at: Optional[datetime] = None


class PaginatedResponseDTO(BaseModel):
    page: int = 1
    page_size: int = 10
    total: int
    data: List[ResponseObjectDTO]


