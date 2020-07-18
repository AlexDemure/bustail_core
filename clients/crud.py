from sqlalchemy import select

from .schemas import ClientCreate
from .models import clients
from db.database import database


async def get_client(attribute: str, value) -> dict:
    query = (
        select([clients])
        .where(getattr(clients.c, attribute) == value)
    )
    data = await database.fetch_one(query)
    return dict(data) if data else dict()


async def create_client(client_data: ClientCreate) -> int:
    query = clients.insert().values(**client_data.dict())
    client_id = await database.execute(query)
    return client_id


async def delete_client(client_id: int):
    query = (
        clients.delete()
        .where(clients.c.id == client_id)
    )
    await database.execute(query)
