from sqlalchemy import DateTime, Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.sql import func

from applications.enums import ApplicationStatus, ApplicationTypes
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
    price = Column(Integer, default=0)
    application_type = Column(String(64), Enum(ApplicationTypes), default=ApplicationTypes.other)
    application_status = Column(String(64), Enum(ApplicationStatus), default=ApplicationStatus.waiting)
    created_at = Column(DateTime, server_default=func.now())
    confirmed_at = Column(DateTime, nullable=True)  # Когда заявка была подтверждена
    expired_at = Column(DateTime, nullable=True)  # Когда заявка истекает


applications = Application.__table__