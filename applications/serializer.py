from typing import List
from applications.schemas import Application, ApplicationWithNotifications


def prepare_applications_with_notifications(application: dict, notifications: List[dict]) -> ApplicationWithNotifications:
    return ApplicationWithNotifications(
        **application,
        notifications=notifications
    )


def prepare_application(application: dict) -> Application:
    return Application(**application)
