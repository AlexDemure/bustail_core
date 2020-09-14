from structlog import get_logger
from typing import Optional
from accounts import schemas, service, serializer, enums
from common.schemas import UpdateBase
from crypt import get_password_hash


class AccountBase:

    schema = None
    logger = None

    def __init__(self, schema):
        self.schema = schema
        self.logger = get_logger()

    async def get_role(self):
        raise NotImplementedError

    async def is_have_account(self) -> bool:
        """Проверка на наличие пользователя в системе"""
        personal_data = await service.PersonalDataService.get_by_attribute('phone', self.schema.personal_data.phone)
        if personal_data:
            return True
        auth_data = await service.AuthorizationDataService.get_by_login(self.schema.authorization_data.login)
        if auth_data:
            return True

        return False

    async def create(self) -> Optional[schemas.AccountData]:
        """Создание аккаунта со всеми связанными таблицами отвечающие за данные пользователя."""
        # Проверка на наличие пользователя в системе
        is_have_account = await self.is_have_account()
        if is_have_account:
            self.logger.debug('Ignored create account')
            return None

        role = await self.get_role()

        account_id = await service.AccountService(self.schema).create()
        self.logger = self.logger.bind(account_id=account_id)
        self.logger.debug("Create account")

        account_role_id = await service.AccountRoleService.create(account_id, role['id'])
        self.logger = self.logger.bind(account_role_id=account_role_id)
        self.logger.debug("Create account role")

        auth_data = self.schema.authorization_data
        hash_password = get_password_hash(auth_data.password)

        auth_data = schemas.AuthorizationDataCreate(
            account_id=account_id,
            login=auth_data.login,
            password=hash_password
        )
        await service.AuthorizationDataService(auth_data).create()
        self.logger.debug("Create authorization data")

        personal_data = schemas.PersonalDataCreate(account_id=account_id, **self.schema.personal_data.dict())
        await service.PersonalDataService(personal_data).create()
        self.logger.debug("Create personal data")

        return await get_account(account_id)


class CreateCustomerAccount(AccountBase):

    async def get_role(self) -> Optional[dict]:
        role = await service.RoleService.get(enums.Roles.customer)
        if not role:
            raise ValueError("Role is not found")

        return role


class CreateArmAccount(AccountBase):

    async def get_role(self) -> Optional[dict]:
        assert isinstance(self.schema, schemas.ArmAccountCreate), 'Schema is wrong format'
        role = await service.RoleService.get(self.schema.role)
        if not role:
            raise ValueError("Role is not found")

        return role


async def get_account(account_id: int) -> Optional[schemas.AccountData]:
    """Получение структуры данных пользователя."""
    account_data = await service.AccountService.get(account_id)
    if account_data:
        return serializer.AccountSerializer.prepared_data(**account_data)
    else:
        return None


async def update_personal_data(schema: UpdateBase):
    """Обновление персональных данных."""
    assert isinstance(schema, UpdateBase), 'Schema is wrong format'

    personal_data = await service.PersonalDataService.get_by_account_id(schema.id)
    if not personal_data:
        raise ValueError("Personal data is not found")

    # В случае если был изменен телефон - обновляем в авторизационных данных логин.
    phone = schema.updated_fields.get('phone', None)
    if phone:
        if personal_data.get('phone', None) != phone:
            auth_data = UpdateBase(
                id=schema.id,
                updated_fields=dict(login=schema.updated_fields['phone'])
            )
            await service.AuthorizationDataService(auth_data).update()

    await service.PersonalDataService(schema).update()


async def update_authorization_data(schema: UpdateBase):
    """Обновление авторизационных данных данных."""
    assert isinstance(schema, UpdateBase), 'Schema is wrong format'
    await service.AuthorizationDataService(schema).update()
