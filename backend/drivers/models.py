from backend.object_storage.enums import FileMimetypes
from tortoise import models, fields

from backend.enums.drivers import TransportType


class Driver(models.Model):
    id = fields.IntField(pk=True)
    account = fields.ForeignKeyField('models.Account', related_name='drivers', on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)
    license_number = fields.CharField(max_length=64, null=True)
    debt = fields.DecimalField(max_digits=10, decimal_places=3)


class Transport(models.Model):
    id = fields.IntField(pk=True)
    driver = fields.ForeignKeyField('models.Driver', related_name='transports', on_delete=fields.CASCADE)
    brand = fields.CharField(max_length=255)
    model = fields.CharField(max_length=255)
    count_seats = fields.IntField(default=1)
    price = fields.IntField(default=0)
    city = fields.CharField(max_length=255)
    state_number = fields.CharField(max_length=16)
    transport_type = fields.CharEnumField(TransportType, max_length=128)


class TransportPhoto(models.Model):
    id = fields.IntField(pk=True)
    transport = fields.ForeignKeyField('models.Transport', related_name='transport_covers', on_delete=fields.CASCADE)
    file_uri = fields.CharField(max_length=255)
    file_hash = fields.CharField(max_length=255)
    media_type = fields.CharEnumField(FileMimetypes, max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)

