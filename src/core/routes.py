from src.modules.application import application_router
from src.modules.jd import jd_router
from src.modules.response import response_router

routes = [application_router, jd_router, response_router]