import uvicorn
from fastapi import FastAPI
from mailing.src.core.config import settings
from mailing.src.routers import router

app = FastAPI(openapi_url=f"{settings.API_URL}/openapi.json", docs_url=f"{settings.API_URL}/docs")


app.include_router(router, prefix=settings.API_URL)


if __name__ == '__main__':
    uvicorn.run("application:app", host="127.0.0.1", port=8001, reload=True, log_level="debug")
