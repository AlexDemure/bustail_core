from typing import Optional
from sqlalchemy import select

from backend.common.crud import CRUDBase
from backend.drivers.models import Driver, Transport
from backend.drivers.schemas import DriverCreate, TransportCreate
from backend.common.schemas import UpdatedBase
from backend.db.database import database


class CRUDDriver(CRUDBase[Driver, DriverCreate, UpdatedBase]):

    async def find_by_account_id(self, account_id: int) -> Optional[dict]:
        query = select([self.model]).where(self.model.account_id == account_id)
        object_model = await database.fetch_one(query)
        return dict(object_model) if object_model else None


driver = CRUDDriver(Driver)


class CRUDTransport(CRUDBase[Transport, TransportCreate, UpdatedBase]):

    async def find_by_params(self, brand: str, model: str, state_number: str) -> Optional[dict]:
        query = select([self.model]).where(
            (self.model.brand == brand) &
            (self.model.model == model) &
            (self.model.state_number == state_number)
        )
        object_model = await database.fetch_one(query)
        return dict(object_model) if object_model else None

    async def get_all_transports(
        self,
        limit: int = 10,
        offset: int = 0,
        city: str = "",
        order_by: str = 'price',
        order_type: str = 'asc',
    ):
        order_by_query = getattr(self.model, order_by)

        if order_type == 'asc':
            order_by_query = order_by_query.asc()
        elif order_type == 'desc':
            order_by_query = order_by_query.desc()
        else:
            raise ValueError("Order type wrong format")

        filter_query = self.model.city.like(f"%{city}%")

        query = (
            select([self.model])
            .where(filter_query)
            .order_by(order_by_query)
            .offset(offset)
            .limit(limit)
        )
        transports = await database.fetch_all(query)
        return [dict(x) for x in transports]


transport = CRUDTransport(Transport)
