from sqlalchemy import select
from accounts.models import accounts, authorization_data, personal_data
from accounts.schemas import AuthorizationDataCreate, PersonalDataCreate
from db.database import database


async def create_account():
    query = accounts.insert().values()
    account_id = await database.execute(query)
    return account_id


async def get_account(account_id: int):
    query = (
        select([accounts, personal_data, authorization_data])
        .where(accounts.c.id == account_id)
    )
    return await database.fetch_one(query)


async def create_authorization_data(data: AuthorizationDataCreate):
    query = authorization_data.insert().values(**data.dict())
    await database.execute(query)


async def get_authorization_data(account_id: int):
    query = authorization_data.select(authorization_data.c.account_id == account_id)
    return await database.fetch_one(query)


async def create_personal_data(data: PersonalDataCreate):
    query = personal_data.insert().values(**data.dict())
    await database.execute(query)


async def get_personal_data(account_id):
    query = personal_data.select(personal_data.c.account_id == account_id)
    return await database.fetch_one(query)
