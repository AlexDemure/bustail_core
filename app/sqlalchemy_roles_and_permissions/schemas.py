

class AccountRoleCreate(BaseModel):
    role_id: int
    account_id: int


class AccountRoleUpdate(UpdateBase):
    pass
