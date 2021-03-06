from typing import Optional, List

from tortoise.query_utils import Q, Prefetch

from backend.common.crud import CRUDBase
from backend.common.schemas import UpdatedBase
from backend.drivers.models import Driver, Transport, TransportPhoto
from backend.notifications.models import Notification
from backend.schemas.drivers import DriverCreate, TransportCreate, TransportPhotoCreate


class CRUDDriver(CRUDBase[Driver, DriverCreate, UpdatedBase]):

    async def get(self, driver_id: int) -> Optional[Driver]:
        return await (
            self.model.filter(id=driver_id).first()
                .prefetch_related(
                Prefetch(
                    'transports',
                    queryset=Transport.all().prefetch_related(
                        Prefetch(
                            'transport_covers',
                            queryset=TransportPhoto.all()
                        )
                    )
                )
            )
        )

    async def find_by_account_id(self, account_id: int) -> Optional[Driver]:
        return await (
            self.model.filter(account_id=account_id).first()
            .prefetch_related(
                Prefetch(
                    'transports',
                    queryset=Transport.all().prefetch_related(
                        Prefetch(
                            'transport_covers',
                            queryset=TransportPhoto.all()
                        )
                    )
                )
            )
        )


driver = CRUDDriver(Driver)


class CRUDTransport(CRUDBase[Transport, TransportCreate, UpdatedBase]):

    async def find_by_params(self, brand: str, model: str, state_number: str) -> Optional[Transport]:
        return await self.model.get_or_none(
            Q(
                Q(brand=brand), Q(model=model), Q(state_number=state_number), join_type="AND"
            )
        )

    async def get_transports_with_notifications(self, driver_id: int):
        return await (
            self.model.filter(driver_id=driver_id).all()
                .prefetch_related(
                Prefetch(
                    'notifications',
                    queryset=Notification.filter(decision__isnull=True).all()
                ),
                Prefetch(
                    'transport_covers',
                    queryset=TransportPhoto.all()
                )
            )
        )

    async def get_all_transports(
        self,
        limit: int = 10,
        offset: int = 0,
        city: str = "",
        order_by: str = 'price',
        order_type: str = 'asc',
    ) -> List[Transport]:

        return await (
            self.model.all()
            .filter(city__icontains=city)
            .order_by(f'{"-" if order_type == "desc" else ""}{order_by}')
            .limit(limit=limit)
            .offset(offset=offset)
            .prefetch_related(Prefetch('transport_covers', queryset=TransportPhoto.all()))
        )


transport = CRUDTransport(Transport)


class CRUDTransportCovers(CRUDBase[TransportPhoto, TransportPhotoCreate, UpdatedBase]):

    async def find_transport_by_hash(self, transport_id: int, file_hash: str) -> Optional[TransportPhoto]:
        return await self.model.get_or_none(
            Q(
                Q(transport_id=transport_id), Q(file_hash=file_hash), join_type="AND"
            )
        )


transport_covers = CRUDTransportCovers(TransportPhoto)
