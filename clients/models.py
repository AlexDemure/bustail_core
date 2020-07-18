from sqlalchemy import DateTime, Column, Integer, ForeignKey
from sqlalchemy.sql import func

from db.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    created_at = Column(DateTime, server_default=func.now())


clients = Client.__table__
