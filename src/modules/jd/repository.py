from src.common.base_repo import BaseRepository
from src.modules.jd.models import JobDescription
from src.modules.jd.dtos import JDObjectDTO, PaginatedJDResponseDTO
from tortoise.expressions import Q


class JDRepository(BaseRepository):
	def __init__(self) -> None:
		super().__init__(JobDescription)



	async def fetch(
		self,
		id: str | None = None,
		search: str | None = None,
		page: int = 1,
		page_size: int = 10,
	) -> PaginatedJDResponseDTO:
		if page < 1 or page_size < 1:
			raise ValueError("page and page_size must be at least 1")

		query = Q()
		if id is not None:
			query &= Q(id=id)
		if search is not None:
			query &= (
				Q(title__icontains=search)
				| Q(description__icontains=search)
				| Q(note_to_intelligence__icontains=search)
			)

		total = await self.model.filter(query).count()
		job_descriptions = await (
			self.model.filter(query)
			.offset((page - 1) * page_size)
			.limit(page_size)
		)

		return PaginatedJDResponseDTO(
			page=page,
			page_size=page_size,
			total=total,
			data=[
				JDObjectDTO.model_validate(job, from_attributes=True)
				for job in job_descriptions
			],
		)
	
	async def agent_fetch(self, id: str) -> JDObjectDTO:
		jd = await self.model.filter(id=id).first()
		if not jd:
			raise ValueError(f"job description with id {id} is not found")
		return JDObjectDTO.model_validate(jd, from_attributes=True)