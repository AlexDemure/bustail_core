from sqlalchemy import DateTime, Column, Integer, String, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func

from backend.db.base_class import Base

from backend.notifications.enums import NotificationTypes


class Notification(Base):
    """Таблица предназначена для сбора уведомлений которые отображаютс в ЛК клиента."""

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("application.id"))
    transport_id = Column(Integer, ForeignKey("transport.id"))
    decision = Column(Boolean, nullable=True)
    notification_type = Column(String(64), Enum(NotificationTypes))
    price = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

