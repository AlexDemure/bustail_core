from backend.drivers.models import Transport
from backend.schemas.drivers import TransportData
from backend.schemas.notifications import NotificationData


def prepare_transports_with_notifications(transport: Transport, notifications: list) -> TransportData:
    return TransportData(
        notifications=[NotificationData(**x.__dict__) for x in notifications],
        **transport.__dict__
    )
