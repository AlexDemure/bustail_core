from sqlalchemy import DateTime, Column, Integer, ForeignKey, String, Enum
from sqlalchemy.sql import func

from drivers.enum import TransportType

from db.database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), unique=True)
    created_at = Column(DateTime, server_default=func.now())


class Transport(Base):
    __tablename__ = "transports"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    type_transport = Column(String(128), Enum(TransportType))
    brand = Column(String(255))
    model = Column(String(255))
    count_seats = Column(Integer)
    price = Column(Integer, default=0)
    state_number = Column(String(64), nullable=True)


drivers = Driver.__table__
transports = Transport.__table__