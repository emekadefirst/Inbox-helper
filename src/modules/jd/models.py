from tortoise import fields
from src.common.base_model import BaseModel


class JobDescription(BaseModel):
    title = fields.CharField(255, null=False, unique=True)
    description = fields.TextField(null=True)
    responseibilities = fields.JSONField(null=True)
    qualifications = fields.JSONField(null=True)
    note_to_intelligence = fields.TextField(null=True) 
    generated_classification = fields.JSONField(null=True) 


    class Meta:
        table = "job_descriptions"
        indexes = [("title", "id")]


