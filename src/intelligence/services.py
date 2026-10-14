from src.common.errors import NotFoundError 
from src.modules.application.repository import ApplicationRepository
from src.modules.jd.repository import JDRepository
from src.modules.response.repository import ResponseRepository
from src.modules.response.models import ResponseStatus  
from src.intelligence.schemas import ClassificationScheme

application_repo = ApplicationRepository()
jd_repo = JDRepository()
response_repo = ResponseRepository()


async def get_application(application_id):
    return await application_repo.get_or_404(id=application_id)


async def get_job(job_id):
    return await jd_repo.get_or_404(id=job_id)


async def save_scheme(job, scheme: ClassificationScheme) -> None:
    await jd_repo.update(job, generated_classification=scheme.model_dump(mode="json"))


async def create_draft(application_id, *, classification: str, reason: str, text: str):
    return await response_repo.create(
        application_id=application_id,
        classification=classification,
        classification_reason=reason,          
        generated_response=text,
        authored_response=text,
        status=ResponseStatus.DRAFT,
    )