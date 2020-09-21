from clients import service, schemas
from accounts.logic import get_account


async def create_client(account_id: int) -> int:
    """Создание клиента."""
    account = await get_account(account_id)
    if not account:
        raise ValueError("Account is not found")

    client = await service.ServiceClient.get(account.id)
    if client:
        return client['id']

    return await service.ServiceClient(schemas.ClientDataCreate(account_id=account.id)).create()

