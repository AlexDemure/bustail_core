from tortoise import models, fields

from backend.enums.applications import ApplicationStatus, ApplicationTypes


class Application(models.Model):

    id = fields.IntField(pk=True)
    account = fields.ForeignKeyField('models.Account', related_name='applications', on_delete=fields.CASCADE)
    driver = fields.ForeignKeyField('models.Driver', related_name='applications', on_delete=fields.CASCADE, null=True)
    to_go_from = fields.CharField(max_length=255)
    to_go_to = fields.CharField(max_length=255, null=True)
    to_go_when = fields.DateField()
    count_seats = fields.IntField(default=1)
    description = fields.CharField(max_length=1024, null=True)
    price = fields.IntField(default=0)
    application_type = fields.CharEnumField(ApplicationTypes, max_length=128)
    application_status = fields.CharEnumField(ApplicationStatus, max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)
    confirmed_at = fields.DatetimeField(null=True)  # Когда заявка была подтверждена
