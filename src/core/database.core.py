from src.configs.database import (
    DB_HOST,
    DB_DATABASE,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
)
from tortoise import Tortoise
from urllib.parse import quote_plus




TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": DB_HOST,
                "port": DB_PORT,
                "user": DB_USER,
                "password": DB_PASSWORD,
                "database": DB_DATABASE,
                "timeout": 8,
            },
        }
    },
    "apps": {
        "models": {
            "models": ["src.core.models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "Africa/Lagos",        
    "minsize": 1,
    "maxsize": 5,  
    "timeout": 10,         
    "max_queries": 500,    
}

