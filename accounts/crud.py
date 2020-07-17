from sqlalchemy import select

from accounts.models import accounts, personal_data
from accounts.schemas import PersonalDataCreate
from authorization.models import authorization_data
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


async def create_personal_data(data: PersonalDataCreate):
    query = personal_data.insert().values(**data.dict())
    await database.execute(query)


async def get_personal_data(attribute: str, value) -> dict:
    query = personal_data.select(getattr(personal_data.c, attribute) == value)
    data = await database.fetch_one(query)
    return dict(data) if data else dict()
