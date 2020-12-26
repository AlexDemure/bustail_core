from typing import List

from tortoise.query_utils import Prefetch

from backend.applications.models import Application
from backend.common.crud import CRUDBase
from backend.common.schemas import UpdatedBase
from backend.notifications.models import Notification
from backend.schemas.applications import ApplicationCreate


class CRUDApplication(CRUDBase[Application, ApplicationCreate, UpdatedBase]):

    async def account_applications(self, account_id: int) -> List[Application]:
        return await (
            self.model.filter(account_id=account_id).all()
            .prefetch_related(
                Prefetch(
                    'notifications',
                    queryset=Notification.all()
                ),
            )
        )

    async def driver_applications(self, driver_id: int) -> List[Application]:
        return await (
            self.model.filter(driver_id=driver_id).all()
            .prefetch_related(
                Prefetch(
                    'notifications',
                    queryset=Notification.all()
                ),
            )
        )

    async def get_all_applications(
        self,
        limit: int = 10,
        offset: int = 0,
        city: str = "",
        order_by: str = 'to_go_when',
        order_type: str = 'asc',
    ) -> List[Application]:
        return await self.model.all()


application = CRUDApplication(Application)
