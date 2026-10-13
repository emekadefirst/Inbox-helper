from tortoise import fields
from enum import Enum
from src.common.base_model import BaseModel

class ProcessingStatus(str, Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"

class Application(BaseModel):
    job = fields.ForeignKeyField(
        "models.JobDescription", related_name="applications", null=True
    )
    from_email = fields.CharField(255, null=False)     
    candidate_name = fields.CharField(255, null=True)
    subject = fields.CharField(500, null=True)
    message = fields.TextField(null=True)
    resume_url = fields.CharField(1000, null=True)
    cover_letter_url = fields.CharField(1000, null=True)
    processing_status = fields.CharEnumField(ProcessingStatus, default=ProcessingStatus.RECEIVED)

    class Meta:
        table = "applications"
        indexes = [("job", "processing_status"), ("from_email", "job")]