from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class JDObjectDTO(BaseModel):
    id: UUID
    title: str = Field(..., max=255)
    description: Optional[str] = None
    responsibilities: Optional[List[str]] = None
    qualifications: Optional[List[str]] = None
    note_to_intelligence: Optional[str] = Field(None, max=255)
    generated_classification: Optional[List[str]] = None 
    created_at: str[datetime]
    updated_at: Optional[str[datetime]] = None


class NestedJDObjectDTO(BaseModel):
    id: UUID
    title: str = Field(..., max=255)


class CreateJDDTO(BaseModel):
   title: str = Field(..., max=255) 
   description: Optional[str] = None
   responsibilities: Optional[List[str]] = None
   qualifications: Optional[List[str]] = None
   note_to_intelligence: Optional[str] = Field(None, max=255)


class PaginatedJDResponseDTO(BaseModel):
    page: int = 1
    page: int = 10
    total: int
    data: List[JDObjectDTO]   
