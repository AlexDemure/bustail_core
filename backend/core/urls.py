from fastapi import APIRouter

from backend.accounts.routers import router as account_router
from backend.applications.routers import router as application_router
from backend.auth.routers import router as auth_router
from backend.common.routers import router as common_router
from backend.drivers.routers import router as driver_router
from backend.mailing.routers import router as mailing_router
from backend.notifications.routers import router as notification_router

api_router = APIRouter()

api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(common_router, tags=["common"])
api_router.include_router(account_router, tags=["accounts"], prefix='/accounts')
api_router.include_router(application_router, tags=["applications"], prefix='/applications')
api_router.include_router(mailing_router, tags=["mailing"], prefix='/mailing')
api_router.include_router(driver_router, tags=["drivers"], prefix='/drivers')
api_router.include_router(notification_router, tags=["notifications"], prefix='/notifications')
