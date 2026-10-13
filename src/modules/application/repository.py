from src.common.base_repo import BaseRepository
from src.modules.application.models import Application
from src.modules.application.dtos import ApplicationObjectDTO, CreateApplicationDTO, PaginatedApplicationDTO

class ApplicationRepository:
    boa = BaseRepository(Application, ApplicationObjectDTO, CreateApplicationDTO, PaginatedApplicationDTO)