from enum import Enum


class NotificationTypes(Enum):
    client_to_driver = "client_to_driver"
    driver_to_client = "driver_to_client"


class NotificationErrors(Enum):
    duplicate_notification = "Данное предложение было ранее отправлено ."
    notification_is_have_decision = "Предложение имеет конечный статус."
