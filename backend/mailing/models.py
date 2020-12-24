from tortoise import models, fields


class SendVerifyCodeEvent(models.Model):

    id = fields.IntField(pk=True)
    account = fields.ForeignKeyField('models.Account', related_name='verify_codes', on_delete=fields.CASCADE)
    message = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)


class ChangePasswordEvent(models.Model):

    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=128)
    message = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
