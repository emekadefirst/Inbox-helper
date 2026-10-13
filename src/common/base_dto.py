from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class BaseDTO(BaseModel):
    id: UUID
    created_at: str[datetime]
    update_at: Optional[str[datetime]] = None

class ErrorResponseDTO(BaseModel):
    message: str
    status: int
    raw_response: Optional[Dict[str, Any]] = None
    time: str[datetime] = datetime.now().isoformat()
