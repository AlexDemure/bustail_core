import random
from typing import Optional

from httpx import AsyncClient

from backend.accounts.crud import account as account_crud
from backend.accounts.models import Account
from backend.common.utils import get_cities
from backend.core.application import app
from backend.db.database import sqlite_db_init
from backend.enums.applications import ApplicationTypes
from backend.enums.drivers import TransportType
from backend.mailing.models import SendVerifyCodeEvent
from backend.permissions.fixtures import setup_permissions_and_roles
from backend.security.utils import generate_random_code
from backend.redis.service import redis
from backend.mailing.service import service_mailing

ASYNC_CLIENT = AsyncClient(app=app, base_url="http://localhost/api/v1")


class TestAccountData:

    email = None
    hashed_password = "string"
    city = "Челябинск"

    def __init__(self):
        self.email = f"{generate_random_code(only_digits=False)}@gmail.com"

    def get_personal_data(self) -> dict:
        return dict(
            email=self.email,
            hashed_password=self.hashed_password,
            city=self.city
        )

    async def get_account_by_email(self) -> Optional[Account]:
        return await account_crud.find_by_email(self.email)

    def get_auth_data(self) -> dict:
        return dict(
            username=self.email,
            password=self.hashed_password
        )


class TestDriverData:

    license_number = generate_random_code(size=16, only_digits=False)

    @staticmethod
    def driver_transports() -> list:
        transports = list()
        for _ in range(5):
            transport_data = {
                "transport_type": random.choice([x.value for x in TransportType]),
                "brand": generate_random_code(size=16, only_digits=False),
                "model": generate_random_code(size=10, only_digits=False),
                "count_seats": random.randint(1, 50),
                "price": random.randint(1000, 10000),
                "city": random.choice(get_cities()),
                "state_number": generate_random_code(size=6, only_digits=False)
            }
            transports.append(transport_data)

        return transports


class TestApplicationData:

    @staticmethod
    def get_applications() -> list:
        applications = list()
        for _ in range(5):
            app = {
                "application_type": random.choice([x.value for x in ApplicationTypes]),
                "to_go_from": random.choice(get_cities()),
                "to_go_to": random.choice(get_cities()),
                "to_go_when": "2021-10-01",
                "count_seats": random.randint(1, 50),
                "description": "string",
                "price": random.randint(10000, 50000)
            }
            applications.append(app)

        return applications


class BaseTest:

    client = ASYNC_CLIENT

    headers = None

    account_data = None

    async def login(self):
        async with ASYNC_CLIENT as ac:
            response = await ac.post("/login/access-token/", data=self.account_data.get_auth_data())

        assert response.status_code == 200
        self.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

    async def create_account(self):
        async with self.client as ac:
            response = await ac.post("/accounts/", json=self.account_data.get_personal_data())

        assert response.status_code == 201
        self.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

        await self.confirm_account()

    @staticmethod
    async def get_verify_code(account_id: int) -> Optional[SendVerifyCodeEvent]:
        return await SendVerifyCodeEvent.get_or_none(account_id=account_id)

    async def confirm_account(self):
        account_object = await self.account_data.get_account_by_email()
        verify_code = await self.get_verify_code(account_object.id)

        async with self.client as ac:
            response = await ac.post("/accounts/confirm/", headers=self.headers, json={"code": verify_code.message})

        assert response.status_code == 200

    async def get_user(self):
        await redis.redis_init()
        await redis.register_service(service_mailing)

        await sqlite_db_init()
        await setup_permissions_and_roles()

        try:
            await self.login()
        except AssertionError:
            await self.create_account()

        async with self.client as ac:
            response = await ac.get("/accounts/me/", headers=self.headers)
        assert response.status_code == 200


