
from sqlalchemy import DateTime, Column, Integer, ForeignKey, String, Enum
from sqlalchemy.sql import func

from backend.drivers.enums import TransportType

from backend.db.base_class import Base


class Driver(Base):
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"), unique=True)
    created_at = Column(DateTime, server_default=func.now())
    license_number = Column(String(64), nullable=True, unique=True)


class Transport(Base):

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("driver.id"))
    type_transport = Column(String(128), Enum(TransportType))
    brand = Column(String(255))
    model = Column(String(255))
    count_seats = Column(Integer, default=1)
    price = Column(Integer, default=0)
    city = Column(String(128))
    state_number = Column(String(16))


class TransportPhoto(Base):
    id = Column(Integer, primary_key=True, index=True)
    transport_id = Column(Integer, ForeignKey("transport.id"))
    file_uri = Column(String(256))
    file_hash = Column(String(128))
    created_at = Column(DateTime, server_default=func.now())