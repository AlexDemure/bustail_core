from typing import TypeVar

from backend.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
