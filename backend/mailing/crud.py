from typing import Optional

from sqlalchemy import select

from backend.common.crud import CRUDBase
from backend.common.schemas import UpdatedBase
from backend.db.database import database
from backend.mailing.models import SendVerifyCodeEvent
from backend.mailing.schemas import SendVerifyCodeEventCreate


class CRUDSendVerifyCode(CRUDBase[SendVerifyCodeEvent, SendVerifyCodeEventCreate, UpdatedBase]):

    async def find_code(self, account_id: int, code: str) -> Optional[dict]:
        query = select([self.model]).where(
            (self.model.verify_code == code) &
            (self.model.account_id == account_id)
        )
        object_model = await database.fetch_one(query)
        return dict(object_model) if object_model else None


send_verify_code_event = CRUDSendVerifyCode(SendVerifyCodeEvent)
