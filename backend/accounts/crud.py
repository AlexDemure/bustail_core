from typing import Optional

from backend.auth.security import verify_password

from backend.accounts.models import Account
from backend.accounts.schemas import AccountCreate, AccountUpdate
from backend.common.crud import CRUDBase


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):

    async def find_by_email(self, email: str) -> Optional[Account]:
        return await self.model.filter(email=email).first()

    async def find_by_phone(self, phone: str) -> Optional[Account]:
        return await self.model.filter(phone=phone).first()

    async def authenticate(self, email: str, password: str) -> Optional[Account]:
        user = await self.find_by_email(email=email)
        if user:
            if verify_password(password, user.hashed_password):
                return user

        return None


account = CRUDAccount(Account)
