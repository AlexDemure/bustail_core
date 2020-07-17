from authorization.crud import create_authorization_data
from authorization.schemas import AuthorizationDataCreate

from .crud import create_personal_data, get_account, create_account
from .schemas import Account
from .schemas import AccountCreate, PersonalDataCreate
from .serializer import AccountSerializer

from crypt import get_password_hash


class AccountView:

    account = None
    auth_data = None
    personal_data = None

    @classmethod
    async def create(cls, account: AccountCreate) -> Account:
        """Создание пользовательского аккаунта с персональными данными и авторизационными."""
        account_id = await create_account()

        auth_data = account.authorization_data
        hash_password = get_password_hash(auth_data.password)

        cls.auth_data = AuthorizationDataCreate(account_id=account_id, login=auth_data.login, password=hash_password)
        cls.personal_data = PersonalDataCreate(account_id=account_id, **account.personal_data.dict())

        await create_authorization_data(cls.auth_data)
        await create_personal_data(cls.personal_data)

        return await cls.get(account_id)

    @staticmethod
    async def get(account_id) -> Account:
        """Получение структуры данных пользователя."""
        account_data = await get_account(account_id)
        return AccountSerializer.prepared_data(**account_data)

