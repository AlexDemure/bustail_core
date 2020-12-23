import pytest
from permissions.fixtures import setup_permissions_and_roles

from backend.db.database import init_db
from backend.tests.data import BaseTest

pytestmark = pytest.mark.asyncio


class TestAccount(BaseTest):

    async def test_create_account(self):
        init_db()
        await setup_permissions_and_roles()

        await self.create_account()
