from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from backend.core.config import settings

MODELS_LIST = [
    "backend.accounts.models", "backend.mailing.models", "backend.drivers.models",
    "backend.applications.models", "backend.notifications.models",
    "backend.permissions.models", "aerich.models"
]


# Необходимо для мигратора aerich
TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URI},
    "apps": {
        "models": {
            "models": MODELS_LIST,
            "default_connection": "default",
        },
    },
}


async def sqlite_db_init():
    await Tortoise.init(
        db_url=settings.DATABASE_URI,
        modules={'models': MODELS_LIST}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


def postgres_db_init(app):
    register_tortoise(
        app,
        db_url=settings.DATABASE_URI,
        modules={"models": MODELS_LIST},
        generate_schemas=True,
        add_exception_handlers=True,
    )
