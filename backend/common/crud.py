from typing import Generic, Optional, Type

from sqlalchemy import select, update, insert

from backend.db.database import database
from backend.common.schemas import CreateSchemaType, UpdateSchemaType
from backend.common.models import ModelType


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, data: CreateSchemaType) -> int:
        query = insert(self.model, data.dict())
        return await database.execute(query)

    async def get(self, object_id: int) -> Optional[dict]:
        query = select([self.model]).where(self.model.id == object_id)
        object_model = await database.fetch_one(query)
        return dict(object_model) if object_model else None

    async def update(self, data: UpdateSchemaType) -> None:
        query = (
            update(self.model)
            .where(self.model.id == data.id)
            .values(**data.updated_fields)
        )
        await database.execute(query)
