from typing import Optional
from sqlalchemy import select, update

from app.crud.base import CRUDBase
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate
from app.db.database import database
from app.core.security import verify_password


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):

    async def find_by_email(self, email: str) -> Optional[dict]:
        query = select([self.model]).where(self.model.email == email)
        object_model = await database.fetch_one(query)
        return dict(object_model) if object_model else None

    async def authenticate(self, email: str, password: str) -> Optional[dict]:
        user = await self.find_by_email(email=email)
        if user:
            user_data = dict(user)

            if verify_password(password, user['hashed_password']):
                return user_data
            return user_data
        return None


account = CRUDAccount(Account)
