from sqlalchemy import DateTime, Column, Integer, String, ForeignKey
from sqlalchemy.sql import func

from db.database import Base


class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    to_go_from = Column(String(255))
    to_go_to = Column(String(255), nullable=True)
    to_go_when = Column(DateTime)
    count_seats = Column(Integer)
    description = Column(String(1024), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    confirmed_at = Column(DateTime, nullable=True)
    expired_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
