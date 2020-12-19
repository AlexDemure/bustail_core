from fastapi import APIRouter

from backend.accounts import account_router
from backend.auth import auth_router
from backend.common import common_router
from backend.applications import application_router
from backend.mailing import mailing_router
from backend.drivers import driver_router

api_router = APIRouter()

api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(common_router, tags=["common"])
api_router.include_router(account_router, tags=["accounts"], prefix='/accounts')
api_router.include_router(application_router, tags=["applications"], prefix='/applications')
api_router.include_router(mailing_router, tags=["mailing"], prefix='/mailing')
api_router.include_router(driver_router, tags=["drivers"], prefix='/driver')