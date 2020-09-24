from typing import List
from drivers.schemas import TransportWithNotifications


def prepare_transport_with_notifications(transport: dict, notifications: List[dict]) -> TransportWithNotifications:
    return TransportWithNotifications(
        **transport,
        notifications=notifications
    )
