from datetime import datetime

from sqlalchemy import DateTime, Column, Integer, ForeignKey

from db.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
