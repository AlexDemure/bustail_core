import pytest
import random
from permissions.fixtures import setup_permissions_and_roles

from backend.db.database import init_db
from backend.tests.data import BaseTest, driver_data

pytestmark = pytest.mark.asyncio


class TestDriver(BaseTest):

    async def test_driver_account(self):
        await self.get_user()

        async with self.client as ac:
            response = await ac.post(
                "/drivers/", headers=self.headers, json={"license_number": driver_data.license_number}
            )
        assert response.status_code == 201

        async with self.client as ac:
            response = await ac.get("/drivers/me/", headers=self.headers)
        assert response.status_code == 200

    async def test_transport(self):
        init_db()
        await setup_permissions_and_roles()

        await self.login()

        async with self.client as ac:
            response = await ac.get("/drivers/me/", headers=self.headers)
        assert response.status_code == 200

        for transport in driver_data.driver_transports():
            async with self.client as ac:
                response = await ac.post("/drivers/transports/", headers=self.headers, json=transport)
            assert response.status_code == 201

            response_json = response.json()

            await self.create_transport_photo(response_json['id'])

    async def create_transport_photo(self, transport_id: int):
        files = ["test_01.jpg", "test_02.jpg", "test_03.jpg", "test_04.jpg"]

        file_name = random.choice(files)
        file_content = open(f"static/test_files/covers/{file_name}", "rb")

        async with self.client as ac:
            response = await ac.post(
                f"/drivers/transports/{transport_id}/covers/",
                headers=self.headers,
                files={'file': (file_name, file_content, 'image/jpeg')}
            )

        assert response.status_code == 201

