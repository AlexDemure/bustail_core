from backend.applications.schemas import ApplicationData
from backend.common.serializer import datetime_to_string


def prepare_application(application: dict) -> ApplicationData:
    return ApplicationData(
        to_go_when=datetime_to_string(application.pop('to_go_when')),
        created_at=datetime_to_string(application.pop('created_at')),
        **application
    )
