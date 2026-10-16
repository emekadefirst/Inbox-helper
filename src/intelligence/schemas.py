from typing import Literal
from pydantic import BaseModel, Field, create_model

class ApplicationResult(BaseModel):         
    classification: str
    reason: str
    draft: str

def result_model_for(labels: list[str]) -> type[BaseModel]:
    """Per-run schema: classification can only be one of this JD's labels."""
    return create_model(
        "ApplicationResult",
        classification=(Literal[tuple(labels)], ...),
        reason=(str, Field(max_length=600)),
        draft=(str, Field(min_length=20, max_length=1200)),
    )