from uuid import UUID
from typing import Optional, List
from src.common.base_dto import BaseDTO
from src.modules.jd.dtos import NestedJDObjectDTO
from pydantic import BaseModel, Field, EmailStr


class CreateApplicationDTO(BaseModel):
    job_id: str = Field(..., max=60)
    from_email: EmailStr = Field(..., max=255)
    candidate_name: str = Field(..., max=255)
    subject: str = Field(..., max=500)
    message: str = Field(None)
    resume_url: str = Field(None, max=255)
    cover_letter_url: str = Field(None, max=1000)


class ApplicationObjectDTO(BaseDTO):
    job: Optional[NestedJDObjectDTO] = None
    from_email: EmailStr = Field(..., max=255)
    candidate_name: Optional[str] = Field(None, max=255)
    subject: Optional[str] = Field(None, max=500)
    message: Optional[str] = None
    resume_url: Optional[str] = Field(None, max=255)
    cover_letter_url: Optional[str] = Field(None, max=1000)


class PaginatedApplicationDTO(BaseModel):
    page: int = 1
    page_size: int = 10
    total: int
    data: List[ApplicationObjectDTO]

class ApplicationNestedDTO(BaseModel):
    id: UUID
    job: Optional[NestedJDObjectDTO] = None
    candidate_name: Optional[str] = Field(None, max=255)