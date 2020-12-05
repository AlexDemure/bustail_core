from enum import Enum


class Permissions(Enum):
    """
    Доступы ограничений в системе
    """
    public_api_access = "public_api_access"
    admin_api_access = "admin_api_access"

    @property
    def description(self):
        if self is self.public_api_access:
            return "Access to all api methods on the client side."
        elif self is self.admin_api_access:
            return "Access to all api methods for the administrator."


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
            return [x for x in Permissions if x != Permissions.admin_api_access]
        elif self is self.admin:
            return [x for x in Permissions if x != Permissions.public_api_access]
