from src.modules.response.dtos import (
	CreateResponseDTO,
	PaginatedResponseDTO,
	ResponseObjectDTO,
	UpdateResponseDTO,
)
from src.modules.response.models import ResponseStatus
from src.modules.response.respository import ResponseRepository


class ResponseService:
	repo = ResponseRepository()

	@classmethod
	async def create(cls, data: CreateResponseDTO) -> ResponseObjectDTO:
		response = await cls.repo.create(**data.model_dump())
		result = await cls.repo.fetch(id=str(response.id), page_size=1)
		return result.data[0]

	@classmethod
	async def fetch(
		cls,
		id: str | None = None,
		search: str | None = None,
		application_id: str | None = None,
		status: ResponseStatus | None = None,
		page: int = 1,
		page_size: int = 10,
	) -> PaginatedResponseDTO:
		return await cls.repo.fetch(
			id=id,
			search=search,
			application_id=application_id,
			status=status,
			page=page,
			page_size=page_size,
		)

	@classmethod
	async def get_by_id(cls, id: str) -> ResponseObjectDTO | None:
		result = await cls.repo.fetch(id=id, page_size=1)
		return result.data[0] if result.data else None

	@classmethod
	async def update(
		cls,
		id: str,
		data: UpdateResponseDTO,
	) -> ResponseObjectDTO | None:
		response = await cls.repo.get(id=id)
		if response is None:
			return None

		values = data.model_dump(exclude_unset=True)
		if values:
			await cls.repo.update(response, **values)

		return await cls.get_by_id(id)

	@classmethod
	async def delete(cls, id: str) -> None:
		await cls.repo.delete(id)
