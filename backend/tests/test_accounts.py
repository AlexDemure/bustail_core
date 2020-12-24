import pytest
from backend.tortoise_roles_and_permissions.permissions.fixtures import setup_permissions_and_roles

from backend.db.database import db_init
from backend.tests.data import BaseTest

pytestmark = pytest.mark.asyncio


class TestAccount(BaseTest):

    async def test_create_account(self):
        await db_init()
        await setup_permissions_and_roles()

        await self.create_account()
