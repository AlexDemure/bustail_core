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
