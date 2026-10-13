from enum import Enum
from tortoise import fields
from src.common.base_model import BaseModel

class ResponseStatus(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    SENT = "sent"

class Response(BaseModel):
    application = fields.ForeignKeyField(
        "models.Application", related_name="responses", null=False
    )
    classification = fields.CharField(100, null=True)   # label from the JD's generated scheme
    classification_reason = fields.TextField(null=True) # reviewer-only, never sent
    generated_response = fields.TextField(null=False)
    authored_response = fields.TextField(null=False)    # starts equal to generated_response
    status = fields.CharEnumField(ResponseStatus, default=ResponseStatus.DRAFT)
    sent_at = fields.DatetimeField(null=True)

    class Meta:
        table = "responses"
        indexes = [("application", "status"), ("classification", "status")]