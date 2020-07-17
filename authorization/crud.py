from db.database import database
from .models import authorization_data
from .schemas import AuthorizationDataCreate


async def create_authorization_data(data: AuthorizationDataCreate):
    query = authorization_data.insert().values(**data.dict())
    await database.execute(query)


async def get_authorization_data(login: str) -> dict:
    query = authorization_data.select(authorization_data.c.login == login)
    data = await database.fetch_one(query)
    return dict(data) if data else dict()