from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core import routes, TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise
from src.configs.app import (
    DEBUG, 
    DOCS_URL, 
    OPENAPI_URL, 
    REDOC_URL, 
    VERSION,
    ACCEPTED_CORE_ORIGIN
)



app = FastAPI(
    title="Inbox Helper",
    version=VERSION,
    debug=DEBUG,
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
    openapi_url=OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ACCEPTED_CORE_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)
for route in routes:
    app.include_router(route)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)