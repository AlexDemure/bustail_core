# Import all the models, so that Base has them before being
# imported by Alembic

from app.db.base_class import Base
from app.models.account import Account
from app.sqlalchemy_roles_and_permissions.models import Role, RolePermission, AccountRole

