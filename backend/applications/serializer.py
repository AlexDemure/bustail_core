from backend.applications.models import Application
from backend.schemas.applications import ApplicationData
from backend.schemas.notifications import NotificationData


def prepare_apps_with_notifications(app: Application, notifications: list) -> ApplicationData:
    return ApplicationData(
        notifications=[NotificationData(**x.__dict__) for x in notifications],
        **app.__dict__
    )
