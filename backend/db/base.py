# Import all the models, so that Base has them before being
# imported by Alembic

from backend.db.base_class import Base
from backend.accounts.models import Account
from backend.drivers.models import Transport, Driver, TransportPhoto
from backend.applications.models import Application
from backend.notifications.models import Notification
from permissions.models import Permission, Role, RolePermission, AccountRole
from backend.mailing.models import SendVerifyCodeEvent


#alembic revision --autogenerate -m ""
#alembic upgrade head