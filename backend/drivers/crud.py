from typing import Optional
from sqlalchemy import select

from backend.common.crud import CRUDBase
from backend.drivers.models import Driver
from backend.drivers.schemas import DriverCreate
from backend.common.schemas import UpdatedBase
from backend.db.database import database


class CRUDDriver(CRUDBase[Driver, DriverCreate, UpdatedBase]):

    async def find_by_account_id(self, account_id: int) -> Optional[dict]:
        query = select([self.model]).where(self.model.account_id == account_id)
        object_model = await database.fetch_one(query)
        return dict(object_model) if object_model else None


driver = CRUDDriver(Driver)
