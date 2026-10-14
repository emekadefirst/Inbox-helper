from typing import Any

from src.modules.jd.dtos import (
    CreateJDDTO,
    JDObjectDTO,
    PaginatedJDResponseDTO,
)
from src.modules.jd.respository import JDRepository


class JDService:
    repo = JDRepository()

    @classmethod
    async def create(cls, data: CreateJDDTO) -> JDObjectDTO:
        values = data.model_dump()
        values["responseibilities"] = values.pop("responsibilities")
        job = await cls.repo.create(data)
        return JDObjectDTO.model_validate(job, from_attributes=True)

    @classmethod
    async def fetch(
        cls,
        id: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedJDResponseDTO:
        return await cls.repo.fetch(
            id=id,
            search=search,
            page=page,
            page_size=page_size,
        )

    @classmethod
    async def get_by_id(cls, id: str) -> JDObjectDTO | None:
        job = await cls.repo.get(id=id)
        if job is None:
            return None
        return JDObjectDTO.model_validate(job, from_attributes=True)

    @classmethod
    async def update(cls, id: str, data: dict[str, Any]) -> JDObjectDTO | None:
        job = await cls.repo.get(id=id)
        if job is None:
            return None

        values = dict(data)
        if "responsibilities" in values:
            values["responseibilities"] = values.pop("responsibilities")
        updated_job = await cls.repo.update(job, **values)
        return JDObjectDTO.model_validate(updated_job, from_attributes=True)

    @classmethod
    async def delete(cls, id: str) -> None:
        await cls.repo.delete(id)