from src.modules.application.repository import ApplicationRepository
from src.modules.jd.repository import JDRepository
from src.modules.response.repository import ResponseRepository 
from langchain.tools import tool
from typing import List
from src.modules.response.models import ResponseStatus

application_repo = ApplicationRepository()
jd_repo = JDRepository()
response_repo = ResponseRepository()


@tool("Get applicant by id", description="Query the application table by id")
async def get_applicant(application_id: str):
    try:
        applicant = await application_repo.agent_fetch(id=application_id)
        if applicant is not None:
            return applicant
        return "applicant_id is not related to any applicant"
    except Exception as error:
        raise ValueError(f"Unknown Error: {error}")


    
@tool("Get job description by id", description="Query the job description table by id")
async def get_job_description(jd_id: str):
    try:
        jd = await jd_repo.agent_fetch(id=jd_id)
        if jd is not None:
            return jd
        return "jd_id is not related to any job description"
    except Exception as error:
        raise ValueError(f"Unknown Error: {error}")

@tool("Generate classification for job description", description="Generate classification for job description")
async def generate_job_decsription_classification(id: str, data: List[str]):
    try:
        jd = await jd_repo.update(id=id, generate_classification=data)
        if jd is not None:
            return "The Job descritpion 'generated_classification' has been updated"
        return "The job description failed to update"
    except Exception as error:
        raise ValueError(f"Unknown Error: {error}")
    

@tool("Generate response for application", description="Generate respoonse an application")
async def generate_application_response(
    application_id: str, 
    classification: str,
    classification_reason: str,
    generated_response: str
    ):
    try:
        response = await response_repo.create(
            application_id=application_id,
            classification=classification,
            classification_reason=classification_reason,
            generated_response=generated_response,
            status=ResponseStatus.DRAFT
        )
        if response is not None:
            return "The Response has been created"
        return "Failed to create the response"
    except Exception as error:
        raise ValueError(f"Unknown Error: {error}")