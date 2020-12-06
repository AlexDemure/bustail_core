from enum import Enum


class NotificationTypes(Enum):
    client_to_driver = "client_to_driver"
    driver_to_client = "driver_to_client"
