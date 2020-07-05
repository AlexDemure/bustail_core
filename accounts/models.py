from datetime import datetime

from sqlalchemy import DateTime, Column, Integer, String, ForeignKey

from db.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    registration_date = Column(DateTime, default=datetime.utcnow)


class AuthorizationData(Base):
    __tablename__ = "authorization_data"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), primary_key=True, index=True)
    login = Column(String(12), unique=True)
    password = Column(String(64))
