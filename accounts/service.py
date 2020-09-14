from sqlalchemy import select, update
from typing import Optional, List
from db.database import database
from accounts import schemas, models, enums
from common.service import BaseService
from common.schemas import UpdateBase


class RoleService(BaseService):

    @staticmethod
    async def get(role_type: enums.Roles) -> Optional[dict]:
        query = select([models.roles]).where(models.roles.c.name == role_type.value)
        role = await database.fetch_one(query)
        return dict(role) if role else None

    @staticmethod
    async def get_all_roles() -> List[dict]:
        """
        Получение списка всех ролей в системе.

        В словарях хранится форма {'id': 1, 'name': 'CUSTOMER', 'description': 'Клиент'}
        """
        roles = await database.fetch_all(models.roles.select())
        if len(roles) > 0:
            return [dict(x) for x in roles]
        else:
            return []

    @staticmethod
    async def create(role_type: enums.Roles, description: str) -> int:
        query = models.roles.insert().values(
            dict(name=role_type.value, description=description)
        )
        return await database.execute(query)


class PermissionService(BaseService):

    @staticmethod
    async def get(permission_id: int) -> Optional[dict]:
        query = select([models.permissions]).where(models.permissions.c.id == permission_id)
        permission = await database.fetch_one(query)
        return dict(permission) if permission else None

    @staticmethod
    async def get_by_permission_type(permission_type: enums.Permissions) -> Optional[dict]:
        query = select([models.permissions]).where(models.permissions.c.name == permission_type.value)
        permission = await database.fetch_one(query)
        return dict(permission) if permission else None

    @staticmethod
    async def get_all_permissions() -> List[dict]:
        """Получение списка всех пермишенов в системе."""
        permissions = await database.fetch_all(models.permissions.select())
        if len(permissions) > 0:
            return [dict(x) for x in permissions]
        else:
            return []

    @staticmethod
    async def create(permission_type: enums.Permissions, description: str) -> int:
        query = models.permissions.insert().values(
            dict(name=permission_type.value, description=description)
        )
        return await database.execute(query)


class RolePermissionService(BaseService):

    @staticmethod
    async def get(role_id: int, permission_id: int) -> Optional[dict]:
        query = (
            select([models.role_permissions])
            .where(
                (models.role_permissions.c.role_id == role_id) &
                (models.role_permissions.c.permission_id == permission_id)
            )
        )
        role_permission = await database.fetch_one(query)
        return dict(role_permission) if role_permission else None

    @staticmethod
    async def get_role_permissions(role_id: int) -> List[dict]:
        query = (
            select([models.role_permissions])
            .where(models.role_permissions.c.role_id == role_id)
        )
        role_permissions = await database.fetch_all(query)
        if len(role_permissions) > 0:
            return [dict(x) for x in role_permissions]
        else:
            return []

    @staticmethod
    async def create(role_id: int, permission_id: int) -> int:
        query = models.role_permissions.insert().values(
            dict(role_id=role_id, permission_id=permission_id)
        )
        return await database.execute(query)


class AccountRoleService(BaseService):

    @staticmethod
    async def get(account_id: int) -> Optional[dict]:
        query = (
            select([models.accounts_role])
            .where(models.accounts_role.c.account_id == account_id)
        )
        account_role = await database.fetch_one(query)
        return dict(account_role) if account_role else None

    @staticmethod
    async def create(account_id: int, role_id: int) -> int:
        query = models.accounts_role.insert().values(
            dict(role_id=role_id, account_id=account_id)
        )
        return await database.execute(query)


class AccountService(BaseService):

    @staticmethod
    async def get(account_id: int) -> Optional[dict]:
        query = (
            select([models.accounts, models.personal_data, models.authorization_data])
            .where(
                (models.accounts.c.id == account_id) &
                (models.personal_data.c.account_id == account_id) &
                (models.authorization_data.c.account_id == account_id)
            )
        )
        account_data = await database.fetch_one(query)
        return dict(account_data) if account_data else None

    @staticmethod
    async def create() -> int:
        query = models.accounts.insert().values()
        account_id = await database.execute(query)
        return account_id

    @staticmethod
    async def delete(account_id: int):
        """Удаление аккаунта со всеми связанными таблицами."""
        delete_personal_data = (
            models.personal_data.delete()
            .where(models.personal_data.c.account_id == account_id)
        )

        delete_auth_data = (
            models.authorization_data.delete()
            .where(models.authorization_data.c.account_id == account_id)
        )

        delete_account_data = (
            models.accounts.delete()
            .where(models.accounts.c.id == account_id)
        )

        queries = [delete_personal_data, delete_auth_data, delete_account_data]
        for query in queries:
            await database.execute(query)


class PersonalDataService(BaseService):

    async def create(self):
        assert isinstance(self.schema, schemas.PersonalDataCreate), 'Schema is wrong format'
        query = models.personal_data.insert().values(**self.schema.dict())
        await database.execute(query)

    @staticmethod
    async def get_by_account_id(account_id: int) -> Optional[dict]:
        query = (
            select([models.personal_data])
            .where(models.personal_data.c.account_id == account_id)
        )
        data = await database.fetch_one(query)
        return dict(data) if data else None

    @staticmethod
    async def get_by_attribute(attribute: str, value, account_id: int = None) -> Optional[dict]:
        """Получение персональных данных по атрибуту модели."""
        query = (
            select([models.personal_data])
            .where(
                (getattr(models.personal_data.c, attribute) == value) &
                (models.personal_data.c.account_id != account_id)
            )
        )
        data = await database.fetch_one(query)
        return dict(data) if data else None

    async def update(self):
        assert isinstance(self.schema, UpdateBase), 'Schema is wrong format'
        query = (
            update(models.personal_data)
            .where(models.personal_data.c.account_id == self.schema.id)
            .values(**self.schema.updated_fields)
        )
        await database.execute(query)


class AuthorizationDataService(BaseService):

    async def create(self):
        assert isinstance(self.schema, schemas.AuthorizationDataCreate), 'Schema is wrong format'
        query = models.authorization_data.insert().values(**self.schema.dict())
        await database.execute(query)

    @staticmethod
    async def get(account_id: int) -> Optional[dict]:
        query = (
            select([models.authorization_data])
            .where(models.authorization_data.c.account_id == account_id)
        )
        data = await database.fetch_one(query)
        return dict(data) if data else None

    @staticmethod
    async def get_by_login(login: str, account_id: int = None) -> Optional[dict]:
        query = (
            select([models.authorization_data])
            .where(
                (models.authorization_data.c.login == login) &
                (models.authorization_data.c.account_id != account_id)
            )
        )
        data = await database.fetch_one(query)
        return dict(data) if data else None

    async def update(self):
        assert isinstance(self.schema, UpdateBase), 'Schema is wrong format'
        query = (
            update(models.authorization_data)
            .where(models.authorization_data.c.account_id == self.schema.id)
            .values(**self.schema.updated_fields)
        )
        await database.execute(query)
