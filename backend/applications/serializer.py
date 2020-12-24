from backend.applications.models import Application
from backend.applications.schemas import ApplicationData
from backend.common.serializer import datetime_to_string


def prepare_application(application: Application) -> ApplicationData:
    data = application.__dict__
    return ApplicationData(
        to_go_when=datetime_to_string(data.pop('to_go_when')),
        created_at=datetime_to_string(data.pop('created_at')),
        **data
    )
