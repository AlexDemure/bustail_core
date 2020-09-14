from sqlalchemy import select, update
from typing import Optional
from db.database import database
from accounts import schemas, models
from common.service import BaseService
from common.schemas import UpdateBase


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

    async def create(self) -> int:
        assert isinstance(self.schema, schemas.PersonalDataCreate), 'Schema is wrong format'
        query = models.personal_data.insert().values(**self.schema.dict())
        return await database.execute(query)

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

    async def create(self) -> int:
        assert isinstance(self.schema, schemas.AuthorizationDataCreate), 'Schema is wrong format'
        query = models.authorization_data.insert().values(**self.schema.dict())
        return await database.execute(query)

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
