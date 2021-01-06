import uvicorn
from fastapi import FastAPI

from backend.core.config import settings
from backend.core.urls import api_router
from backend.db.database import sqlite_db_init, postgres_db_init
from backend.mailing.service import service_mailing
from backend.permissions.fixtures import setup_permissions_and_roles
from backend.redis.service import redis

app = FastAPI(openapi_url=f"{settings.API_URL}/openapi.json", docs_url=f"{settings.API_URL}/docs")


if settings.ENV == "PROD":
    print("Connect to PostgreSQL DB")
    postgres_db_init(app)


@app.on_event("startup")
async def db_init():
    if settings.ENV == "DEV":
       print("Connect to SQLITE DB")
       await sqlite_db_init()


@app.on_event("startup")
async def redis_init():
    await redis.redis_init()
    await redis.register_service(service_mailing)


@app.on_event("startup")
async def fixtures():
    await setup_permissions_and_roles()


app.include_router(api_router, prefix=settings.API_URL)


if __name__ == '__main__':
    uvicorn.run("application:app", host="127.0.0.1", port=8002, reload=True, log_level="debug")
