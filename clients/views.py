from typing import Optional
from clients import crud
from clients.schemas import ClientCreate, Client


class ClientView:

    @staticmethod
    async def create(client_data: ClientCreate) -> int:
        """Создание пользовательского аккаунта с персональными данными и авторизационными."""
        client_id = await crud.create_client(client_data)
        return client_id

    @staticmethod
    async def get(attribute, value) -> Optional[Client]:
        """Получение структуры данных пользователя."""
        client_data = await crud.get_client(attribute, value)
        if client_data:
            return Client(**client_data)
        else:
            return None

    @staticmethod
    async def delete(client_id: int) -> None:
        await crud.delete_client(client_id)
