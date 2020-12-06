from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime

from backend.db.base_class import Base


class Account(Base):
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(128), nullable=False)
    phone = Column(String(16), nullable=False)
    city = Column(String(64), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    created_at = Column(DateTime, server_default=func.now())