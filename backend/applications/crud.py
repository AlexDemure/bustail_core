from sqlalchemy import select

from backend.common.crud import CRUDBase
from backend.db.database import database
from backend.applications.models import Application
from backend.applications.schemas import ApplicationCreate
from backend.applications.enums import ApplicationStatus
from backend.common.schemas import UpdatedBase


class CRUDApplication(CRUDBase[Application, ApplicationCreate, UpdatedBase]):

    async def account_applications(self, account_id: int) -> list:
        query = (
            select([self.model])
            .where(self.model.account_id == account_id)
        )
        applications = await database.fetch_all(query)
        return [dict(x) for x in applications]

    async def driver_applications(self, driver_id: int) -> list:
        query = (
            select([self.model])
            .where(self.model.driver_id == driver_id)
        )
        applications = await database.fetch_all(query)
        return [dict(x) for x in applications]

    async def get_all_applications(
        self,
        limit: int = 10,
        offset: int = 0,
        city: str = "",
        order_by: str = 'to_go_when',
        order_type: str = 'asc',
    ):
        order_by_query = getattr(self.model, order_by)

        if order_type == 'asc':
            order_by_query = order_by_query.asc()
        elif order_type == 'desc':
            order_by_query = order_by_query.desc()
        else:
            raise ValueError("Order tyep wrong format")

        filter_query = (
            (
                (self.model.to_go_from.like(f"%{city}%")) |
                (self.model.to_go_to.like(f"%{city}%"))
            ) & (self.model.application_status == ApplicationStatus.waiting.value)
        )

        query = (
            select([self.model])
            .where(filter_query)
            .order_by(order_by_query)
            .offset(offset)
            .limit(limit)
        )
        applications = await database.fetch_all(query)
        return [dict(x) for x in applications]


application = CRUDApplication(Application)
