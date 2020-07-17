from sqlalchemy import DateTime, Column, Integer, String, ForeignKey, Date
from sqlalchemy.sql import func

from db.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    registration_date = Column(DateTime, server_default=func.now())


accounts = Account.__table__


class PersonalData(Base):
    __tablename__ = "personal_data"

    account_id = Column(Integer, ForeignKey("accounts.id"), primary_key=True, index=True)
    fullname = Column(String(255))
    phone = Column(String(12))
    email = Column(String(64), nullable=True)
    birthday = Column(Date, nullable=True)
    city = Column(String(128))


personal_data = PersonalData.__table__