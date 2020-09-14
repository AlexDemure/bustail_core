from typing import Optional
from accounts import schemas, service, serializer
from common.schemas import UpdateBase
from crypt import get_password_hash


async def get_account(account_id: int) -> Optional[schemas.AccountData]:
    """Получение структуры данных пользователя."""
    account_data = await service.AccountService.get(account_id)
    if account_data:
        return serializer.AccountSerializer.prepared_data(**account_data)
    else:
        return None


async def create_account(schema: schemas.AccountCreate) -> Optional[schemas.AccountData]:
    """Создание пользовательского аккаунта с персональными данными и авторизационными."""
    assert isinstance(schema, schemas.AccountCreate), 'Schema is wrong format'

    account_id = await service.AccountService(schema).create()

    auth_data = schema.authorization_data
    hash_password = get_password_hash(auth_data.password)

    auth_data = schemas.AuthorizationDataCreate(
        account_id=account_id,
        login=auth_data.login,
        password=hash_password
    )
    await service.AuthorizationDataService(auth_data).create()

    personal_data = schemas.PersonalDataCreate(account_id=account_id, **schema.personal_data.dict())
    await service.PersonalDataService(personal_data).create()

    return await get_account(account_id)


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
