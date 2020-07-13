from accounts import crud
from .serializer import AccountSerializer
from .schemas import (
    AccountCreate, AuthorizationDataCreate, PersonalDataCreate,
)


class AccountView:

    account = None
    auth_data = None
    personal_data = None

    @classmethod
    async def create(cls, account: AccountCreate):
        account_id = await crud.create_account()
        cls.auth_data = AuthorizationDataCreate(account_id=account_id, **account.authorization_data.dict())
        cls.personal_data = PersonalDataCreate(account_id=account_id, **account.personal_data.dict())

        await crud.create_authorization_data(cls.auth_data)
        await crud.create_personal_data(cls.personal_data)

        return await cls.get(account_id)

    @staticmethod
    async def get(account_id):
        account_data = await crud.get_account(account_id)
        if not account_data:
            return None

        return AccountSerializer.prepared_data(**account_data)


