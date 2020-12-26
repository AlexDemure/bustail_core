from backend.applications.models import Application
from backend.applications.schemas import ApplicationData
from backend.common.serializer import datetime_to_string


def prepare_application(application: Application) -> ApplicationData:
    data = application.__dict__
    return ApplicationData(**data)
