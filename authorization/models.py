from sqlalchemy import Column, Integer, String, ForeignKey

from db.database import Base


class AuthorizationData(Base):
    __tablename__ = "authorization_data"

    account_id = Column(Integer, ForeignKey("accounts.id"), primary_key=True, index=True)
    login = Column(String(12), unique=True)
    password = Column(String(64))


authorization_data = AuthorizationData.__table__
