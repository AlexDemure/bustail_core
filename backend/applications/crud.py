from backend.common.crud import CRUDBase
from backend.applications.models import Application
from backend.applications.schemas import ApplicationCreate
from backend.common.schemas import UpdatedBase


class CRUDApplication(CRUDBase[Application, ApplicationCreate, UpdatedBase]):
    pass


application = CRUDApplication(Application)
