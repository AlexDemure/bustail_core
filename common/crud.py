from db.database import database


async def create_object_model(model, data: dict) -> int:
    query = model.insert().values(**data)
    return await database.execute(query)
