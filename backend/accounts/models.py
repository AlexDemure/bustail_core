from tortoise import models, fields


class Account(models.Model):
    id = fields.IntField(pk=True)
    fullname = fields.CharField(max_length=255, null=True)
    email = fields.CharField(max_length=128, null=False, unique=True)
    phone = fields.CharField(max_length=16, null=True)
    city = fields.CharField(max_length=64, null=False)
    hashed_password = fields.CharField(max_length=128, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    verified_at = fields.DatetimeField(null=True)
