from sqlalchemy import DateTime, Column, Integer, String, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func

from db.database import Base
from notifications.enums import NotificationTypes


class Notifications(Base):
    """Таблица предназначена для сбора уведомлений которые отображаютс в ЛК клиента."""
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    transport_id = Column(Integer, ForeignKey("transports.id"))
    decision = Column(Boolean, nullable=True)
    notification_type = Column(String(64), Enum(NotificationTypes))
    price = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())


notifications = Notifications.__table__