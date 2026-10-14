from tortoise import migrations
from tortoise.migrations import operations as ops
import functools
from aerich.coder import decoder, encoder
from json import dumps, loads
from src.modules.application.models import ProcessingStatus
from src.modules.response.models import ResponseStatus
from tortoise.fields.base import OnDelete
from uuid import uuid4
from tortoise import fields
from tortoise.indexes import Index

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='Aerich',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('version', fields.CharField(max_length=255)),
                ('app', fields.CharField(max_length=100)),
                ('content', fields.JSONField(encoder=encoder, decoder=decoder)),
            ],
            options={'table': 'aerich', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='JobDescription',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(null=True, auto_now=False, auto_now_add=False)),
                ('title', fields.CharField(unique=True, max_length=255)),
                ('description', fields.TextField(null=True, unique=False)),
                ('responseibilities', fields.JSONField(null=True, encoder=functools.partial(dumps, separators=(',', ':')), decoder=loads)),
                ('qualifications', fields.JSONField(null=True, encoder=functools.partial(dumps, separators=(',', ':')), decoder=loads)),
                ('note_to_intelligence', fields.TextField(null=True, unique=False)),
                ('generated_classification', fields.JSONField(null=True, encoder=functools.partial(dumps, separators=(',', ':')), decoder=loads)),
            ],
            options={'table': 'job_descriptions', 'app': 'models', 'indexes': [Index(fields=['title', 'id'])], 'pk_attr': 'id'},
            bases=['BaseModel'],
        ),
        ops.CreateModel(
            name='Application',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(null=True, auto_now=False, auto_now_add=False)),
                ('job', fields.ForeignKeyField('models.JobDescription', source_field='job_id', null=True, db_constraint=True, to_field='id', related_name='applications', on_delete=OnDelete.CASCADE)),
                ('from_email', fields.CharField(max_length=255)),
                ('candidate_name', fields.CharField(null=True, max_length=255)),
                ('subject', fields.CharField(null=True, max_length=500)),
                ('message', fields.TextField(null=True, unique=False)),
                ('resume_url', fields.CharField(null=True, max_length=1000)),
                ('cover_letter_url', fields.CharField(null=True, max_length=1000)),
                ('processing_status', fields.CharEnumField(default=ProcessingStatus.RECEIVED, description='RECEIVED: received\nPROCESSING: processing\nDONE: done\nFAILED: failed', enum_type=ProcessingStatus, max_length=10)),
            ],
            options={'table': 'applications', 'app': 'models', 'indexes': [Index(fields=['job', 'processing_status']), Index(fields=['from_email', 'job'])], 'pk_attr': 'id'},
            bases=['BaseModel'],
        ),
        ops.CreateModel(
            name='Response',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(null=True, auto_now=False, auto_now_add=False)),
                ('application', fields.ForeignKeyField('models.Application', source_field='application_id', db_constraint=True, to_field='id', related_name='responses', on_delete=OnDelete.CASCADE)),
                ('classification', fields.CharField(null=True, max_length=100)),
                ('classification_reason', fields.TextField(null=True, unique=False)),
                ('generated_response', fields.TextField(unique=False)),
                ('authored_response', fields.TextField(unique=False)),
                ('status', fields.CharEnumField(default=ResponseStatus.DRAFT, description='DRAFT: draft\nAPPROVED: approved\nSENT: sent', enum_type=ResponseStatus, max_length=8)),
                ('sent_at', fields.DatetimeField(null=True, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'responses', 'app': 'models', 'indexes': [Index(fields=['application', 'status']), Index(fields=['classification', 'status'])], 'pk_attr': 'id'},
            bases=['BaseModel'],
        ),
    ]
