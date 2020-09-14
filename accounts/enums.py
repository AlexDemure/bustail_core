from enum import Enum


class EnumWChoices(Enum):

    @classmethod
    def as_choices(cls):
        return [(enum_element.value, enum_element.description) for enum_element in cls]


class Roles(EnumWChoices):
    """
    Типы пользователей в системе
    """
    customer = "CUSTOMER"
    identifier = "IDENTIFIER"
    admin = "ADMIN"

    @property
    def description(self):
        if self is self.customer:
            return "Клиент"
        elif self is self.identifier:
            return "Идентификатор"
        elif self is self.admin:
            return "Администратор системы"


class Permissions(EnumWChoices):
    """
    Доступы ограничений в системе
    """
    public_api_access = "public_api_access"  # Доступ ко всем апи-методам на стороне клиента

    arm_api_access = "arm_api_access"  # Доступ ко всем апи-методам на стороне ARM

    @property
    def description(self):
        if self is self.public_api_access:
            return "Доступ ко всем апи-методам на стороне клиента."
        elif self is self.arm_api_access:
            return "Доступ ко всем апи-методам для ARM."
