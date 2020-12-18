from sqlalchemy import DateTime, Column, Integer, String, ForeignKey
from sqlalchemy.sql import func

from backend.db.base_class import Base


class SendVerifyCodeEvent(Base):

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"))
    message = Column(String(16))
    created_at = Column(DateTime, server_default=func.now())


class ChangePasswordEvent(Base):

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), nullable=False)
    message = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
