from src.modules.response.dtos import CreateResponseDTO
from src.modules.jd.repository import JDRepository
from src.modules.application.repository import ApplicationRepository
from src.modules.response.repository import ResponseRepository

class JDTool:
    repo = JDRepository()

    @classmethod
    async def get_or_404(cls, id: str):
        job = await cls.repo.get(id=id)
        if job is None:
            raise ValueError(f"Job with id {id} not found")
        return job

    @classmethod
    async def update_jd_generated_classification(
        cls,
        id: str,
        classification: str,
    ) -> None:
        job = await cls.repo.get(id=id)
        if job is None:
            raise ValueError(f"Job with id {id} not found")
        await cls.repo.update(job, generated_classification=classification)

class ApplicationTool:
    repo = ApplicationRepository()

    @classmethod
    async def get_or_404(cls, id: str):
        application = await cls.repo.get(id=id)
        if application is None:
            raise ValueError(f"Application with id {id} not found")
        return application

class ResponseTool:
    repo = ResponseRepository()

    @classmethod
    async def write(cls, data: CreateResponseDTO):
        response = await cls.repo.create(**data.model_dump())
        if response is None:
            raise ValueError(f"Response with id {data.id} not found")
        return response

tools = [
    JDTool.get_or_404,
    JDTool.update_jd_generated_classification,
    ApplicationTool.get_or_404,
    ResponseTool.get_or_404,
    ResponseTool.write,
]
