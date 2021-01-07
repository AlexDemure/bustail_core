from typing import List
from backend.drivers.models import Transport, TransportPhoto
from backend.schemas.drivers import TransportData
from backend.schemas.notifications import NotificationData


def prepare_transports_with_notifications(transport: Transport, notifications: list) -> TransportData:
    return TransportData(
        notifications=[NotificationData(**x.__dict__) for x in notifications],
        **transport.__dict__
    )


def prepare_transport_with_photos(transport: Transport, photos: List[TransportPhoto]) -> TransportData:
    return TransportData(
        transport_covers=[dict(id=x.id) for x in photos],
        **transport.__dict__
    )
