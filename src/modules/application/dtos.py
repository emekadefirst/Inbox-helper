from uuid import UUID
from typing import Any, Optional, List
from src.common.base_dto import BaseDTO
from src.modules.jd.dtos import NestedJDObjectDTO, JDObjectDTO
from src.modules.application.models import ProcessingStatus
from pydantic import BaseModel, Field, EmailStr, field_validator


class CreateApplicationDTO(BaseModel):
    job_id: str = Field(..., max=60)
    from_email: EmailStr = Field(..., max=255)
    candidate_name: str = Field(..., max=255)
    subject: str = Field(..., max=500)
    message: str = Field(None)
    resume_url: Optional[str] = Field(None, max=1000)
    cover_letter_url: Optional[str] = Field(None, max=1000)


class ApplicationObjectDTO(BaseDTO):
    job: Optional[NestedJDObjectDTO] = None
    processing_status: ProcessingStatus
    from_email: EmailStr = Field(..., max=255)
    candidate_name: Optional[str] = Field(None, max=255)
    subject: Optional[str] = Field(None, max=500)
    message: Optional[str] = None
    resume_url: Optional[str] = Field(None, max=255)
    cover_letter_url: Optional[str] = Field(None, max=1000)

class AgentApplicationObjectDTO(BaseModel):
    job: JDObjectDTO
    from_email: EmailStr = Field(..., max=255)
    candidate_name: Optional[str] = Field(None, max=255)
    subject: Optional[str] = Field(None, max=500)
    message: Optional[str] = None
    resume_url: Optional[str] = Field(None, max=255)
    cover_letter_url: Optional[str] = Field(None, max=1000)


class ApplicationImportRow(BaseModel):
    from_email: EmailStr
    candidate_name: str | None = Field(None, max_length=255)
    subject: str | None = Field(None, max_length=500)
    message: str | None = Field(None, max_length=10_000)       # cap what reaches the LLM
    job_title: str | None = None
    resume_url: str | None = Field(None, max_length=1000)
    cover_letter_url: str | None = Field(None, max_length=1000)

    @field_validator("resume_url", "cover_letter_url")
    @classmethod
    def https_only(cls, v):
        if v and not v.lower().startswith("https://"):
            raise ValueError("must be an https URL")
        return v


class ImportReportDTO(BaseModel):
    total: int
    created: int = 0
    skipped_duplicates: int = 0
    errors: list[dict[str, Any]] = Field(default_factory=list)
    created_ids: list[UUID] = Field(default_factory=list)


class PaginatedApplicationDTO(BaseModel):
    page: int = 1
    page_size: int = 10
    total: int
    data: List[ApplicationObjectDTO]

class ApplicationNestedDTO(BaseModel):
    id: UUID
    job: Optional[NestedJDObjectDTO] = None
    candidate_name: Optional[str] = Field(None, max=255)