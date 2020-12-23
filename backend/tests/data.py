import random

from httpx import AsyncClient
from security_utils.security import generate_random_code
from sqlalchemy import select

from backend.accounts.models import Account
from backend.common.utils import get_cities
from backend.core.application import app
from backend.db.database import database
from backend.drivers.enums import TransportType
from backend.mailing.models import SendVerifyCodeEvent


ASYNC_CLIENT = AsyncClient(app=app, base_url="http://localhost/api/v1")


class TestAccountData:

    email = f"{generate_random_code(only_digits=False)}@gmail.com"
    hashed_password = "string"
    city = "Челябинск"

    def get_personal_data(self) -> dict:
        return dict(
            email=self.email,
            hashed_password=self.hashed_password,
            city=self.city
        )

    async def get_account_by_email(self) -> dict:
        query = select([Account]).where(Account.email == self.email)
        object_model = await database.fetch_one(query)
        return dict(object_model) if object_model else None

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


account_data = TestAccountData()

driver_data = TestDriverData()


class BaseTest:

    client = ASYNC_CLIENT

    headers = None

    async def login(self):
        async with ASYNC_CLIENT as ac:
            response = await ac.post("/login/access-token/", data=account_data.get_auth_data())

        assert response.status_code == 200
        self.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

    async def create_account(self):
        async with self.client as ac:
            response = await ac.post("/accounts/", json=account_data.get_personal_data())

        assert response.status_code == 201
        self.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

        await self.confirm_account()

    @staticmethod
    async def get_verify_code(account_id: int) -> dict:
        query = select([SendVerifyCodeEvent]).where(SendVerifyCodeEvent.account_id == account_id)
        object_model = await database.fetch_one(query)
        return dict(object_model) if object_model else None

    async def confirm_account(self):
        account_object = await account_data.get_account_by_email()
        verify_code = await self.get_verify_code(account_object['id'])

        async with self.client as ac:
            response = await ac.post("/accounts/confirm/", headers=self.headers, json={"code": verify_code['message']})

        assert response.status_code == 200

        await self.get_user()

    async def get_user(self):
        async with self.client as ac:
            response = await ac.get("/accounts/me/", headers=self.headers)
        assert response.status_code == 200

