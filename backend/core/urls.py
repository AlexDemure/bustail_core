from fastapi import APIRouter

from backend.accounts import account_router
from backend.auth import auth_router

api_router = APIRouter()

api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(account_router, tags=["accounts"], prefix='/accounts')
