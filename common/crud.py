from sqlalchemy import select
from typing import Optional

from db.database import database


async def create_object_model(model, data: dict) -> int:
    query = model.insert().values(**data)
    return await database.execute(query)


async def get_object_model(model, id: int) -> Optional[dict]:
    query = select([model]).where(model.c.id == id)
    object_model = await database.fetch_one(query)
    return dict(object_model) if object_model else None
