import pytest
import random
from backend.permissions.fixtures import setup_permissions_and_roles

from backend.db.database import db_init
from backend.tests.data import BaseTest, TestAccountData, TestDriverData, TestApplicationData
from backend.notifications.enums import NotificationTypes

pytestmark = pytest.mark.asyncio


class AccountProfile(BaseTest):

    account_data = TestAccountData()
    application_data = TestApplicationData()

    async def create_client_account(self):
        await self.create_account()

    async def create_applications(self):
        await self.get_user()

        applications_id = list()

        for app in self.application_data.get_applications():
            async with self.client as ac:
                response = await ac.post(
                    "/applications/", headers=self.headers, json=app
                )
            assert response.status_code == 201
            response_json = response.json()
            applications_id.append(response_json['id'])

        return applications_id


class DriverProfile(BaseTest):

    account_data = TestAccountData()
    driver_data = TestDriverData()

    async def create_driver_account(self):
        await self.create_account()

        async with self.client as ac:
            response = await ac.post(
                "/drivers/", headers=self.headers, json={"license_number": self.driver_data.license_number}
            )
        assert response.status_code == 201

    async def create_driver_transports(self):

        transports_id = list()
        for transport in self.driver_data.driver_transports():
            async with self.client as ac:
                response = await ac.post("/drivers/transports/", headers=self.headers, json=transport)
            assert response.status_code == 201

            response_json = response.json()
            transports_id.append(response_json['id'])

        return transports_id


class TestNotification(BaseTest):

    async def test_notification(self):
        await db_init()
        await setup_permissions_and_roles()

        driver_profile = DriverProfile()
        client_profile = AccountProfile()

        await driver_profile.create_driver_account()
        transports_id = await driver_profile.create_driver_transports()

        await client_profile.create_client_account()
        applications_id = await client_profile.create_applications()

        notification_driver_to_client = [(transports_id[i], applications_id[i]) for i in range(5)]
        notification_client_to_driver = [(applications_id[i], transports_id[i]) for i in range(5)]

        for notification in notification_driver_to_client:
            # Создание уведомления от водителя к клиенту
            async with self.client as ac:
                response = await ac.post(
                    "notifications/",
                    headers=driver_profile.headers,
                    json=dict(
                        transport_id=notification[0],
                        application_id=notification[1],
                        notification_type=NotificationTypes.driver_to_client.value,
                        price=random.randint(10000, 50000),
                    )
                )
            assert response.status_code == 201
            response_json = response.json()

            # Установка решения по заявке со стороны клиента
            async with self.client as ac:
                response = await ac.put(
                    "notifications/",
                    headers=client_profile.headers,
                    json=dict(
                        notification_id=response_json['id'],
                        decision=random.choice([True, False])
                    )
                )
            assert response.status_code == 200

        # Создание заявки от клиента водителю
        for notification in notification_client_to_driver:
            async with self.client as ac:
                response = await ac.post(
                    "notifications/",
                    headers=client_profile.headers,
                    json=dict(
                        transport_id=notification[1],
                        application_id=notification[0],
                        notification_type=NotificationTypes.client_to_driver.value,
                        price=None
                    )
                )
            assert response.status_code == 201
            response_json = response.json()

            # Установка решения по заявке со стороны клиента
            async with self.client as ac:
                response = await ac.put(
                    "notifications/",
                    headers=driver_profile.headers,
                    json=dict(
                        notification_id=response_json['id'],
                        decision=random.choice([True, False])
                    )
                )
            assert response.status_code == 200
