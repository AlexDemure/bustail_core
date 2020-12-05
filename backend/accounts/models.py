from sqlalchemy import Column, Integer, String

# Автоматический импорт
from backend.db.base_class import Base


class Account(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
