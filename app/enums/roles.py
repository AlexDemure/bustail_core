from enum import Enum
from app.enums import EnumPermissions


class Roles(Enum):
    """
    Типы пользователей в системе
    """
    customer = "Customer"
    admin = "Admin"

    @property
    def description(self):
        if self is self.customer:
            return "Customer"
        elif self is self.admin:
            return "Admin"

    def get_permissions(self):
        if self is self.customer:
            return [x for x in EnumPermissions if x != EnumPermissions.admin_api_access]
        elif self is self.admin:
            return [x for x in EnumPermissions if x != EnumPermissions.public_api_access]
