from sqlalchemy import DateTime, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.sql import func
from applications.enums import ApplicationStatus
from notifications.enums import NotificationTypes
from db.database import Base


class Notifications(Base):
    """Таблица предназначена для сбора уведомлений которые отображаютс в ЛК клиента."""
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    transport_id = Column(Integer, ForeignKey("transports.id"))
    status = Column(String(64), Enum(ApplicationStatus), default=ApplicationStatus.waiting)
    notification_type = Column(String(64), Enum(NotificationTypes))
    price = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())


notifications = Notifications.__table__