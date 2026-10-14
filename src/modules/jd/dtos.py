from uuid import UUID
from src.common.base_dto import BaseDTO
from typing import Optional, List
from pydantic import AliasChoices, BaseModel, Field

class JDObjectDTO(BaseDTO):
    title: str = Field(..., max=255)
    description: Optional[str] = None
    responsibilities: Optional[List[str]] = Field(
        None,
        validation_alias=AliasChoices("responsibilities", "responseibilities"),
    )
    qualifications: Optional[List[str]] = None
    note_to_intelligence: Optional[str] = Field(None, max=255)
    generated_classification: Optional[List[str]] = None 



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
    page_size: int = 10
    total: int
    data: List[JDObjectDTO]   
