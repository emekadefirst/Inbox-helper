from src.configs.database import DATABASE_URL




TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.aiosqlite",
            "credentials": {
                "file_path": DATABASE_URL,
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
}

