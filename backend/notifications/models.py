from tortoise import models, fields

from backend.enums.notifications import NotificationTypes


class Notification(models.Model):
    """Таблица предназначена для сбора уведомлений которые отображаютс в ЛК клиента."""

    id = fields.IntField(pk=True)
    application = fields.ForeignKeyField('models.Application', related_name='notifications', on_delete=fields.CASCADE)
    transport = fields.ForeignKeyField('models.Transport', related_name='notifications', on_delete=fields.CASCADE)
    decision = fields.BooleanField(null=True)
    notification_type = fields.CharEnumField(NotificationTypes, max_length=128)
    price = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

