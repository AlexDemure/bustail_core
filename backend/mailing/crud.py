from typing import Optional
from tortoise.query_utils import Q
from sqlalchemy import select

from backend.common.crud import CRUDBase
from backend.common.schemas import UpdatedBase

from backend.mailing.models import SendVerifyCodeEvent, ChangePasswordEvent
from backend.mailing.schemas import SendVerifyCodeEventCreate, ChangePasswordEventCreate


class CRUDSendVerifyCode(CRUDBase[SendVerifyCodeEvent, SendVerifyCodeEventCreate, UpdatedBase]):

    async def find_code(self, account_id: int, code: str) -> Optional[SendVerifyCodeEvent]:
        return await self.model.get_or_none(
            Q(
                Q(message=code),
                Q(account_id=account_id),
                join_type="AND"
            )
        )

send_verify_code_event = CRUDSendVerifyCode(SendVerifyCodeEvent)


class CRUDChangePassword(CRUDBase[ChangePasswordEvent, ChangePasswordEventCreate, UpdatedBase]):

    async def find_token(self, email: str, token: str) -> Optional[dict]:
        return await self.model.get_or_none(
            Q(
                Q(message=token),
                Q(email=email),
                join_type="AND"
            )
        ).first()


change_password_event = CRUDChangePassword(ChangePasswordEvent)
