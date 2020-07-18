from sqlalchemy import select, update

from accounts.models import accounts, personal_data, authorization_data
from accounts.schemas import (
    PersonalDataCreate, AuthorizationDataCreate,
    AuthorizationDataUpdate, PersonalDataUpdate
)
from db.database import database


async def create_account():
    query = accounts.insert().values()
    account_id = await database.execute(query)
    return account_id


async def get_account(account_id: int) -> dict:
    query = (
        select([accounts, personal_data, authorization_data])
        .where(
            (accounts.c.id == account_id) &
            (personal_data.c.account_id == account_id) &
            (authorization_data.c.account_id == account_id)
        )
    )
    account_data = await database.fetch_one(query)
    return dict(account_data) if account_data else dict()


async def delete_account(account_id: int):
    delete_personal_data = (
        personal_data.delete()
        .where(personal_data.c.account_id == account_id)
    )

    delete_auth_data = (
        authorization_data.delete()
        .where(authorization_data.c.account_id == account_id)
    )

    delete_account_data = (
        accounts.delete()
        .where(accounts.c.id == account_id)
    )

    queries = [delete_personal_data, delete_auth_data, delete_account_data]
    for query in queries:
        await database.execute(query)


async def create_personal_data(data: PersonalDataCreate):
    query = personal_data.insert().values(**data.dict())
    await database.execute(query)


async def get_personal_data(attribute: str, value, account_id: int = None) -> dict:
    query = (
        select([personal_data])
        .where(
            (getattr(personal_data.c, attribute) == value) &
            (personal_data.c.account_id != account_id)
        )
    )
    data = await database.fetch_one(query)
    return dict(data) if data else dict()


async def update_personal_data(update_data: PersonalDataUpdate):
    query = (
        update(personal_data)
        .where(personal_data.c.account_id == update_data.account_id)
        .values(**update_data.dict())
    )
    await database.execute(query)


async def create_authorization_data(data: AuthorizationDataCreate):
    query = authorization_data.insert().values(**data.dict())
    await database.execute(query)


async def get_authorization_data(login: str, account_id: int = None) -> dict:
    query = (
        select([authorization_data])
        .where(
            (authorization_data.c.login == login) &
            (authorization_data.c.account_id != account_id)
        )
    )
    data = await database.fetch_one(query)
    return dict(data) if data else dict()


async def update_auth_data(update_data: AuthorizationDataUpdate):
    query = (
        update(authorization_data)
        .where(authorization_data.c.account_id == update_data.account_id)
        .values(**update_data.dict())
    )
    await database.execute(query)
