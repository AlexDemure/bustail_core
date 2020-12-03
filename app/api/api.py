from fastapi import APIRouter

from app.api.endpoints import login, accounts

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(accounts.router, tags=["accounts"], prefix='/accounts')