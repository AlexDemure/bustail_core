import uvicorn

from fastapi import FastAPI

from app.api.api import api_router
from app.core.config import settings
from app.db.database import database
from app.sqlalchemy_roles_and_permissions.fixtures import setup_permissions_and_roles

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    await setup_permissions_and_roles()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(api_router, prefix=settings.API_URL)


if __name__ == '__main__':
    uvicorn.run("application:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
