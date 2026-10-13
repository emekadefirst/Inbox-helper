from uuid import UUID
from datetime import datetime
from typing import Optional, List
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


class ApplicationObjectDTO(BaseModel):
    id: UUID
    job: NestedJDObjectDTO
    from_email: EmailStr = Field(..., max=255)
    candidate_name: str = Field(..., max=255)
    subject: str = Field(..., max=500)
    message: Optional[str] = None
    resume_url: Optional[str] = Field(None, max=255)
    cover_letter_url: Optional[str] = Field(None, max=1000)
    created_at: str[datetime]
    updated_at: Optional[str[datetime]] = None

class PaginatedApplicationDTO(BaseModel):
    page: int = 1
    page: int = 10
    total: int
    data: List[ApplicationObjectDTO]

class ApplicationNestedDTO(BaseModel):
    id: UUID
    job: NestedJDObjectDTO
    candidate_name: str = Field(..., max=255)