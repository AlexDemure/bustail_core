import pytest
from httpx import AsyncClient, Response
from security_utils.security import generate_random_code
from sqlalchemy import select

from backend.accounts.models import Account
from backend.core.application import app
from backend.db.database import database
from backend.db.database import init_db
from backend.mailing.models import SendVerifyCodeEvent


pytestmark = pytest.mark.asyncio


class TestAccountData:

    email = f"{generate_random_code(only_digits=False)}@gmail.com"
    hashed_password = "string"
    city = "Челябинск"

    def get_personal_data(self):
        return dict(
            email=self.email,
            hashed_password=self.hashed_password,
            city=self.city
        )

    async def get_account_by_email(self) -> dict:
        query = select([Account]).where(Account.email == self.email)
        object_model = await database.fetch_one(query)
        return dict(object_model) if object_model else None


class TestAccount:

    client = AsyncClient(app=app, base_url="http://localhost/api/v1")

    account_data = TestAccountData()

    headers = None

    async def test_create_account(self):
        init_db()

        async with self.client as ac:
            response = await ac.post("/accounts/", json=self.account_data.get_personal_data())

        assert response.status_code == 201
        self.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

        await self.confirm_account()

    @staticmethod
    async def get_verify_code(account_id: int) -> dict:
        query = select([SendVerifyCodeEvent]).where(SendVerifyCodeEvent.account_id == account_id)
        object_model = await database.fetch_one(query)
        return dict(object_model) if object_model else None

    async def confirm_account(self):
        account_object = await self.account_data.get_account_by_email()
        verify_code = await self.get_verify_code(account_object['id'])

        async with self.client as ac:
            response = await ac.post("/accounts/confirm/", headers=self.headers, json={"code": verify_code['message']})

        assert response.status_code == 200

        await self.get_user()

    async def get_user(self):
        async with self.client as ac:
            response = await ac.get("/accounts/me/", headers=self.headers)
        assert response.status_code == 200
