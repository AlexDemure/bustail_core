import pytest

from backend.tests.data import BaseTest, application_data

pytestmark = pytest.mark.asyncio


class TestApplications(BaseTest):

    async def test_applications(self):
        await self.get_user()

        for app in application_data.get_applications():
            async with self.client as ac:
                response = await ac.post(
                    "/applications/", headers=self.headers, json=app
                )
            assert response.status_code == 201




