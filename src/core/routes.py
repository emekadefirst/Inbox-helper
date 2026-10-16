from src.modules.application.routes import application_router
from src.modules.jd.routes import jd_router
from src.modules.response.routes import response_router

routes = [application_router, jd_router, response_router]