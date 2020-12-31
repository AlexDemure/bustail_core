import pytest
from backend.permissions.fixtures import setup_permissions_and_roles

from backend.db.database import sqlite_db_init
from backend.tests.data import BaseTest, TestAccountData
from backend.redis.service import redis
from backend.mailing.service import service_mailing
pytestmark = pytest.mark.asyncio


class TestAccount(BaseTest):

    account_data = TestAccountData()

    async def test_create_account(self):
        await redis.redis_init()
        await redis.register_service(service_mailing)

        await sqlite_db_init()
        await setup_permissions_and_roles()

        await self.create_account()
