from sqlalchemy import select

from backend.common.crud import CRUDBase
from backend.db.database import database
from backend.applications.models import Application
from backend.applications.schemas import ApplicationCreate
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



application = CRUDApplication(Application)
